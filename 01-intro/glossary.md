# GenAI Glossary

Terms are selected from report.md and explained in my own words.

**LLM (Large Language Model)** — Neural network which is trained on a huge amount of text. Its sole role is to predict what text should be next. LLM powers AI technologies such as ChatGPT, Claude, Copilot. "Large" in LLM refers to its billions of parameters, the internal values the model learned during training.

**Token** — It is a tiny piece of text which LLM works with. It is neither a word nor a letter, but something in between. For instance a word "testing" might be one token, and a word "unbelievable" might be as three tokens. In practice it matters because you pay per token, and model limits are also counted in tokens.

**Next-token prediction** — Principle of generation when a model analyzes the whole text before this exact moment and chooses the most probable next token. Then it adds it into the text and repeats the process. That’s how a chain of guesses turns into a coherent answer. This is exactly what Aliaksandr Tsurko meant in our first online session by “looping this output as the next input”.

**Context window** — How many tokens a model can see at once: prompt, chat history, attached files. Model simply doesn’t know anything that doesn’t fit into it. It works like short-term memory, not long-term memory.

**Hallucination** — Model confidently gives false information: non-existent product, made up link, false quotation. The reason lies exactly in next-token prediction: model chooses probable but not reliable or proven. That's why we gave an agent a list of products with relevant links.

**Prompt** — Input text which you give to model: question, instruction, context, examples. The quality of an answer strongly depends on the prompt. It’s like a bug report: the more precise the steps and expected result, the better the outcome.

**RAG (Retrieval-Augmented Generation)** — Model does not know your internal documents: company knowledge, Confluence, Jira. RAG firstly searches for needed pieces in these documents (retrieval), puts them in the prompt (augmented) and only then model generates answer (generation). This reduces hallucinations, and answers rely on real data. Example from my report: Atlassian Rovo.

**Embedding** — Text turned into a list of numbers (vector) in a way that texts with similar meaning get similar numbers. "How to return the order" and "make a refund" end up close to each other even though there is no common words. RAG search relies on embeddings. It matches by meaning, not by exact words: by context, but not exact word coincidence.

**AI agent** — LLM that not only answers in texts but acts, plans steps, uses tools (files, terminal, search, API) looks at the result and decides what to do next. This is exactly what Copilot does today in Agent mode, it creates folders and files by itself.

**Multimodal model** — Model that works not only with texts but with pictures, audio and video. For example you give it a screenshot of an app and it finds layout bugs. Multimodality in our lecture was described as a combination of specialized modules for every type of data.

**AI coding assistant** — AI built into a tool you already use, usually an IDE. It suggests code, writes tests and explains errors. In our lecture this was called the "plugin/companion approach", unlike AI-native tools such as Cursor, where AI is the center of everything. GitHub Copilot is the best-known example.

**Vibe coding** — A way of development where you describe what you want in plain language, and AI writes all the code. You don't go deep into details yourself. The plus is speed. The minus is that you may not understand what you got, and you can miss bugs or security holes. As a QA, I see this as a new source of work for testers, not less.

**Static analysis** — Checking code without running it: looking for bugs, vulnerabilities and style issues just by reading the code itself. Classic linters work by fixed rules, while AI reviewers like CodeRabbit also understand the context of the change.

**Root cause analysis (RCA)** — Finding the real reason of a problem, not just the symptom. The symptom is "checkout fails". The root cause is "after the deploy, the payment service ran out of memory". AI tools like Datadog Bits AI speed this up by connecting logs, metrics and deploys. For me as a QA this feels like the next step after a bug report.

**Visual regression testing** — Comparing UI screenshots before and after changes to catch visual bugs: a shifted button, cut-off text, broken layout. Simple pixel-by-pixel comparison gives a lot of false alarms, while AI tools like Applitools can tell real changes from noise.