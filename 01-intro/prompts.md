# How I used AI in this task

I used GitHub Copilot in VS Code (Agent mode) to set up the repo structure and get a first draft of the report.
Everything else I did myself:

- picked the 8 use cases (I wanted to cover the whole dev cycle, and several of them are close to my own QA work)
- found and checked the products for each use case before giving them to the agent, so it couldn't make up names or links
- read the draft, rewrote the parts I didn't agree with and fixed the wording
- wrote the glossary by hand; used Claude to fix grammar
- clicked through every link in the report before submitting

Below are the prompts I gave to Copilot.

---

## Prompt 1: repo structure

```
Set up this repo for my GenAI course.
Create a folder 01-intro/ with a subfolder 01-intro/graph/.
Add a .gitignore for a Python project (__pycache__/, .venv/, *.pyc, .vscode/, .idea/).
Don't create anything else yet.
```

## Prompt 2: report draft

```
Now create 01-intro/report.md. It's a research report on how GenAI is used in software development.

Short intro at the top, short conclusion at the end.
One "##" section per use case. For each one write 1-2 paragraphs about:
business value, technical challenges, weak points.
Then a "### Existing implementations" list in this format:
- **Name** - [link](URL) - one sentence about what it does

Use ONLY the products I list below. Don't add your own and don't change the links,
I already checked them. Don't make up any numbers or statistics.

1. Code generation & AI coding assistants
   - GitHub Copilot - https://github.com/features/copilot
   - Cursor - https://cursor.com
   - Claude Code - https://www.anthropic.com/claude-code
2. Test generation & QA automation
   - Diffblue Cover - https://www.diffblue.com/cover
   - Qodo - https://www.qodo.ai
   - mabl - https://www.mabl.com
3. Code review & static analysis
   - CodeRabbit - https://www.coderabbit.ai
   - Amazon CodeGuru Reviewer - https://aws.amazon.com/codeguru/
   - Snyk Code - https://snyk.io/product/snyk-code/
4. Log analysis & incident / bug triage
   - Datadog Bits AI SRE - https://www.datadoghq.com/product/ai/bits-ai-sre/
   - Dynatrace Davis AI - https://www.dynatrace.com/platform/artificial-intelligence/
   - PagerDuty AIOps - https://www.pagerduty.com/platform/aiops/
5. Requirements analysis & documentation
   - Atlassian Intelligence in Jira - https://www.atlassian.com/software/jira/ai
   - Mintlify - https://mintlify.com
   - Swimm - https://swimm.io
6. RAG-based knowledge assistants
   - Atlassian Rovo - https://www.atlassian.com/software/rovo
   - Glean - https://www.glean.com
   - Notion AI - https://www.notion.com/product/ai
7. Customer support chatbots in e-commerce
   - Klarna AI Assistant (case study) - https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/
   - Intercom Fin - https://fin.ai
   - Zendesk AI agents - https://www.zendesk.com/service/ai/
8. Multimodal apps (vision, speech, visual UI testing)
   - Applitools Eyes - https://applitools.com
   - OpenAI Whisper - https://github.com/openai/whisper
   - Be My Eyes (Be My AI) - https://www.bemyeyes.com

Keep the English simple and professional.
```