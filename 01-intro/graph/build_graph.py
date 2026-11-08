"""
Builds a relationship graph between glossary terms and the sections of report.md.

- explicit usage: the term itself (or its abbreviation) is written in the text
- implicit usage: the idea is there, but in other words (synonyms from terms.json)

Output: terms_stats.json (raw numbers) and terms_graph.png (graph + bar chart).
Run:  python build_graph.py
"""

import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

HERE = Path(__file__).parent
REPORT = HERE.parent / "report.md"
TERMS = HERE / "terms.json"


def split_sections(text):
    """Returns {section title: section text}. Text before the first '##' is the intro."""
    sections = {}
    title = "Introduction"
    buf = []
    for line in text.splitlines():
        if line.startswith("## "):
            sections[title] = "\n".join(buf)
            title = line[3:].strip()
            buf = []
        elif not line.startswith("# "):
            buf.append(line)
    sections[title] = "\n".join(buf)
    return sections


def make_pattern(phrase):
    # Short all-caps abbreviations (LLM, RAG, RCA) must match case-sensitively,
    # otherwise "rag" inside other words or lowercase noise could be counted.
    flags = 0 if phrase.isupper() else re.IGNORECASE
    # (?:s|es)? lets "token" also match "tokens"
    return re.compile(r"\b" + re.escape(phrase) + r"(?:s|es)?\b", flags)


def count_usage(text, terms):
    """
    Counts explicit and implicit mentions of every term in one piece of text.
    Every match is masked so the same words are never counted twice.
    Order matters: explicit forms go first (a synonym must not "steal" the term itself),
    and inside each group longer phrases go first, so "root cause analysis"
    is not counted again as "root cause" and "next-token prediction" not as "token".
    """
    patterns = []
    for term, forms in terms.items():
        for kind in ("explicit", "implicit"):
            for phrase in forms[kind]:
                priority = 0 if kind == "explicit" else 1
                patterns.append((priority, -len(phrase), term, kind, make_pattern(phrase)))
    patterns.sort(key=lambda p: (p[0], p[1]))

    counts = {t: {"explicit": 0, "implicit": 0} for t in terms}
    masked = list(text)
    for _, _, term, kind, pattern in patterns:
        for m in pattern.finditer("".join(masked)):
            counts[term][kind] += 1
            masked[m.start():m.end()] = "#" * (m.end() - m.start())
    return counts


def main():
    report = REPORT.read_text(encoding="utf-8")
    terms = json.loads(TERMS.read_text(encoding="utf-8"))["terms"]
    sections = split_sections(report)

    # per-section counts -> graph edges; totals -> node sizes and bar chart
    per_section = {name: count_usage(body, terms) for name, body in sections.items()}
    totals = {t: {"explicit": 0, "implicit": 0} for t in terms}
    for counts in per_section.values():
        for t, c in counts.items():
            totals[t]["explicit"] += c["explicit"]
            totals[t]["implicit"] += c["implicit"]

    (HERE / "terms_stats.json").write_text(
        json.dumps({"totals": totals, "per_section": per_section}, indent=2),
        encoding="utf-8",
    )

    print(f"{'Term':<28}{'Explicit':>10}{'Implicit':>10}")
    for t, c in sorted(totals.items(), key=lambda x: -(x[1]["explicit"] + x[1]["implicit"])):
        print(f"{t:<28}{c['explicit']:>10}{c['implicit']:>10}")

    # ---- graph: terms on the left, report sections on the right ----
    G = nx.Graph()
    for t in terms:
        G.add_node(t, kind="term")
    for s in sections:
        G.add_node(s, kind="section")
    for s, counts in per_section.items():
        for t, c in counts.items():
            weight = c["explicit"] + c["implicit"]
            if weight:
                G.add_edge(t, s, weight=weight, explicit=c["explicit"], implicit=c["implicit"])

    term_nodes = sorted(terms, key=lambda t: -(totals[t]["explicit"] + totals[t]["implicit"]))
    section_nodes = list(sections)
    pos = {}
    for i, t in enumerate(term_nodes):
        pos[t] = (0, -i * len(section_nodes) / len(term_nodes))
    for i, s in enumerate(section_nodes):
        pos[s] = (1, -i)

    fig, (ax_graph, ax_bar) = plt.subplots(
        1, 2, figsize=(20, 11), gridspec_kw={"width_ratios": [2.2, 1]}
    )

    # edge colour shows which kind of mention dominates in that section
    edge_colors, edge_widths = [], []
    for u, v, d in G.edges(data=True):
        edge_colors.append("#2b6cb0" if d["explicit"] >= d["implicit"] else "#dd6b20")
        edge_widths.append(0.8 + d["weight"] * 0.9)

    nx.draw_networkx_edges(G, pos, ax=ax_graph, edge_color=edge_colors,
                           width=edge_widths, alpha=0.55)
    nx.draw_networkx_nodes(
        G, pos, nodelist=term_nodes, ax=ax_graph, node_color="#2b6cb0",
        node_size=[250 + 90 * (totals[t]["explicit"] + totals[t]["implicit"]) for t in term_nodes],
    )
    nx.draw_networkx_nodes(G, pos, nodelist=section_nodes, ax=ax_graph,
                           node_color="#718096", node_shape="s", node_size=300)

    for t in term_nodes:
        x, y = pos[t]
        label = f"{t}  (E:{totals[t]['explicit']} / I:{totals[t]['implicit']})"
        ax_graph.text(x - 0.07, y, label, ha="right", va="center", fontsize=10)
    for s in section_nodes:
        x, y = pos[s]
        ax_graph.text(x + 0.05, y, s, ha="left", va="center", fontsize=10)

    ax_graph.set_title("Glossary terms -> report sections\n"
                       "blue edge = mostly explicit, orange edge = mostly implicit, "
                       "thicker = more mentions", fontsize=12)
    ax_graph.set_xlim(-0.9, 1.9)
    ax_graph.axis("off")

    # ---- bar chart: explicit vs implicit per term ----
    names = term_nodes[::-1]
    exp = [totals[t]["explicit"] for t in names]
    imp = [totals[t]["implicit"] for t in names]
    ax_bar.barh(names, exp, color="#2b6cb0", label="Explicit")
    ax_bar.barh(names, imp, left=exp, color="#dd6b20", label="Implicit")
    for i, (e, im) in enumerate(zip(exp, imp)):
        ax_bar.text(e + im + 0.2, i, f"{e} / {im}", va="center", fontsize=9)
    ax_bar.set_title("Usage frequency in report.md", fontsize=12)
    ax_bar.set_xlabel("mentions")
    ax_bar.legend(loc="lower right")
    ax_bar.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    out = HERE / "terms_graph.png"
    plt.savefig(out, dpi=120)
    print(f"\nSaved: {out}")


if __name__ == "__main__":
    main()
