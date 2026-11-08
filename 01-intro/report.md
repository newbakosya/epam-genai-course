# GenAI in Software Development

Generative AI is now used in almost every part of software development, from writing code to investigating incidents and answering customers. Most of these tools are built on an LLM (Large Language Model) that works through next-token prediction: it reads the prompt and everything in its context window, and generates the most probable continuation, token by token. This explains both the strength and the main risk of GenAI. It is fast and flexible, but it can produce a hallucination, a confident answer that is simply wrong.

In this report I look at eight use cases. For each one I describe the business value, the technical challenges and the weak points, and list real products that already do it. As a QA engineer, I paid extra attention to where these tools can fail, because that is where testing and human review are still needed.

## Code generation & AI coding assistants

**Business value.** An AI coding assistant suggests code, explains errors and writes routine parts of a project directly in the IDE. Developers spend less time on boilerplate and more on design and problem solving. Newer tools also work as an AI agent: they plan the task, edit several files, run commands and check the result by themselves. Vibe coding goes even further, where a person only describes what they want and the AI writes the whole thing.

**Challenges and weak points.** The assistant has to understand the existing code, project conventions and what the user actually means, all within a limited context window. Generated code can look correct but contain bugs or security holes, and with vibe coding the developer may not fully understand what was produced. In my view, this does not reduce the need for testing, it increases it: every generated change still has to be reviewed and tested like code written by a person.

### Existing implementations
- **GitHub Copilot** - [link](https://github.com/features/copilot) - AI assistant built into the IDE that offers code completions, chat and an agent mode that can edit files on its own.
- **Cursor** - [link](https://cursor.com) - AI-native code editor where the AI is the main way of interacting with the codebase, not an add-on.
- **Claude Code** - [link](https://www.anthropic.com/claude-code) - Agentic coding tool that works in the terminal, reads the project, edits files and runs commands to complete a task.

## Test generation & QA automation

**Business value.** GenAI can generate unit tests, suggest test cases from requirements and help maintain automated test suites. Teams reach higher coverage faster and catch regressions earlier, while testers spend less time on repetitive test writing.

**Challenges and weak points.** The hardest part is making tests check the *expected* behavior, not just the current one. If the code already has a bug, a generated test can simply "lock in" that bug as correct. AI also tends to cover the obvious happy path and miss the edge cases that real users hit. From my experience testing an e-commerce app, the most expensive bugs are usually in flows like payment, promo codes and order status changes, and a tool that only reads the code does not know which flows matter most to the business. Generated tests are a good starting point, but a tester still has to decide what is important to check.

### Existing implementations
- **Diffblue Cover** - [link](https://www.diffblue.com/cover) - Autonomously writes and maintains Java unit tests and can run fully inside the company's environment, so code does not leave the organization.
- **Qodo** - [link](https://www.qodo.ai) - AI platform for code integrity that generates tests and reviews code changes in the IDE and pull requests.
- **mabl** - [link](https://www.mabl.com) - Low-code test automation platform for web, mobile and API testing that uses AI to help create and maintain tests.

## Code review & static analysis

**Business value.** Static analysis checks code without running it, looking for bugs, vulnerabilities and style problems. AI reviewers add an understanding of context: they summarize a pull request, comment on specific lines and suggest fixes. Reviews become faster, and human reviewers can focus on architecture and logic.

**Challenges and weak points.** The system must tell real problems from harmless patterns. Too many false alarms and developers start ignoring the tool; too few and real issues slip through. A clean AI review does not prove the code is correct or secure. It is one more filter, not a replacement for a human decision.

### Existing implementations
- **CodeRabbit** - [link](https://www.coderabbit.ai) - Reviews every pull request, writes a summary of the changes and leaves line-by-line comments with suggested fixes.
- **Amazon CodeGuru Reviewer** - [link](https://aws.amazon.com/codeguru/) - AWS service that analyzes code to find defects and security issues and recommends improvements.
- **Snyk Code** - [link](https://snyk.io/product/snyk-code/) - Security-focused static analysis tool that finds vulnerabilities in source code and suggests how to fix them.

## Log analysis & incident / bug triage

**Business value.** During an incident, engineers have to search through logs, metrics, alerts and recent deploys. AI tools connect this information and help with root cause analysis (RCA): finding the real reason of a problem, not just the symptom. This shortens the time to recovery and reduces the stress of on-call work.

**Challenges and weak points.** The result is only as good as the data. If logs are incomplete or inconsistent, the AI may point to the wrong cause and sound very convincing about it. Its suggestions should be treated as hypotheses that a person checks before acting, especially when the action affects production. For QA this area is close to daily work: a good bug report already contains the logs and steps, and AI can help turn them into a likely root cause faster.

### Existing implementations
- **Datadog Bits AI SRE** - [link](https://www.datadoghq.com/product/ai/bits-ai-sre/) - AI agent that autonomously investigates alerts, analyzes telemetry and posts root cause findings in Slack and the incident timeline.
- **Dynatrace Davis AI** - [link](https://www.dynatrace.com/platform/artificial-intelligence/) - AI engine in the Dynatrace platform that analyzes observability data to detect problems and identify their root cause.
- **PagerDuty AIOps** - [link](https://www.pagerduty.com/platform/aiops/) - Groups related alerts and reduces noise so incident responders can see what actually matters.

## Requirements analysis & documentation

**Business value.** GenAI can summarize meetings and discussions, turn rough ideas into structured requirements or user stories, and generate technical documentation from code. Knowledge becomes easier to find, and teams spend less time on repetitive writing.

**Challenges and weak points.** A summary can quietly drop an important constraint or make an open question sound like a final decision. For a tester this is dangerous, because test cases are built from requirements: a lost detail in the requirement becomes a missed bug later. Generated documentation also goes out of date quickly unless it is connected to the code and reviewed.

### Existing implementations
- **Atlassian Intelligence in Jira** - [link](https://www.atlassian.com/software/jira/ai) - AI features in Jira that help write and summarize issues, break work into tasks and search project information in natural language.
- **Mintlify** - [link](https://mintlify.com) - Documentation platform that uses AI to help write, maintain and search developer documentation.
- **Swimm** - [link](https://swimm.io) - Keeps documentation coupled to the code, so it updates or flags when the related code changes.

## RAG-based knowledge assistants

**Business value.** A normal LLM does not know a company's internal documents. RAG (Retrieval-Augmented Generation) solves this: it first searches the company's sources, puts the relevant pieces into the prompt, and only then generates the answer. The search usually works through embeddings, so it finds documents by meaning, not only by exact words. Employees get answers from Confluence, Jira or shared drives in seconds instead of searching manually.

**Challenges and weak points.** Quality depends on the sources and on retrieval. If the right passage is not found, or the document is outdated, the answer will be wrong even if the model itself is good. Permissions are critical: the assistant must never show a user information they are not allowed to see. Users should always be able to open the source and check it.

### Existing implementations
- **Atlassian Rovo** - [link](https://www.atlassian.com/software/rovo) - AI search, chat and agents that find knowledge across Jira, Confluence and connected third-party apps while respecting user permissions.
- **Glean** - [link](https://www.glean.com) - Enterprise AI search and assistant that connects to many workplace apps and answers questions from company knowledge.
- **Notion AI** - [link](https://www.notion.com/product/ai) - AI built into Notion that answers questions, summarizes and writes using the content of a team's workspace.

## Customer support chatbots in e-commerce

**Business value.** Support chatbots answer common questions about orders, delivery, refunds and payments 24/7 and pass complex cases to human agents. Customers get answers faster, and the support team handles fewer repetitive requests. Klarna is a well-known example: in its first month, its AI assistant handled about two-thirds of customer service chats.

**Challenges and weak points.** The bot needs accurate, current data about orders and policies, and the right to perform only safe actions. A hallucination here is expensive: a wrong answer about a refund or a delivery date directly hurts the customer and the brand. Having worked as the only QA on a grocery delivery app, I see testing such a bot as a real challenge: there is no single correct answer to compare against, so testers need to check whether answers are factually correct, safe and polite, and whether the bot hands over to a human at the right moment.

### Existing implementations
- **Klarna AI Assistant (case study)** - [link](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/) - Klarna's announcement about its OpenAI-powered assistant handling two-thirds of customer service chats in its first month.
- **Intercom Fin** - [link](https://fin.ai) - AI customer service agent that answers customer questions using a company's help content and hands over to people when needed.
- **Zendesk AI agents** - [link](https://www.zendesk.com/service/ai/) - AI agents in Zendesk that resolve common support requests and assist human agents.

## Multimodal apps (vision, speech, visual UI testing)

**Business value.** A multimodal model works not only with text, but also with images, audio and video. This enables speech recognition, image description for accessibility, and visual regression testing, where the tool compares screenshots of an app before and after a change to catch layout bugs.

**Challenges and weak points.** Inputs vary a lot: accents and noise in audio, different screen sizes and devices in UI. Models can misread a visual detail or a spoken word. In visual regression testing, simple pixel comparison gives many false alarms, while too loose comparison misses real bugs. For mobile apps, where the same screen looks different on iOS and Android, this balance is especially important.

### Existing implementations
- **Applitools Eyes** - [link](https://applitools.com) - Visual AI testing tool that compares app screenshots like a human eye would, ignoring noise and catching meaningful UI changes.
- **OpenAI Whisper** - [link](https://github.com/openai/whisper) - Open-source speech recognition model that transcribes and translates audio in many languages.
- **Be My Eyes (Be My AI)** - [link](https://www.bemyeyes.com) - App that uses AI to describe photos and surroundings for people who are blind or have low vision.

## Conclusion

GenAI already helps at every stage of software development: writing code, testing, reviewing, investigating incidents, documenting and supporting users. But all these tools share the same base, an LLM that predicts probable text, so all of them can be confidently wrong. The teams that benefit most are the ones that give the model good data, verify its output and keep people responsible for important decisions. For me as a QA engineer, this means the role of testing is not disappearing. It is moving towards checking AI-generated work and testing AI-based features themselves.
