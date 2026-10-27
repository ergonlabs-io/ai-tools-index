# AI Tools Index

A maintained index of the AI tools developers actually use: coding agents, app builders, MCP servers, and the infrastructure underneath them.

Unlike most lists, every entry is structured data. Stars, last activity and license are refreshed from GitHub nightly, and archived or inactive projects are flagged automatically instead of rotting in place. Each tool gets a permanent dex number, Pokédex-style, that never changes or gets reused.

**107 tools** · updated 2026-10-27 · [contribute](CONTRIBUTING.md)

☁️ hosted service (everything else installs and runs on your machine) · 🆕 added in the last 30 days · 💤 no commits in 180 days · 🗄️ archived on GitHub

## Contents

- [Coding agents](#coding-agents)
  - [Terminal agents](#terminal-agents)
  - [Editor agents](#editor-agents)
  - [Cloud and autonomous agents](#cloud-and-autonomous-agents)
  - [Code review](#code-review)
- [App builders](#app-builders)
  - [Hosted](#hosted)
  - [Open source and local](#open-source-and-local)
- [MCP servers](#mcp-servers)
  - [Developer tools](#developer-tools)
  - [Platforms and services](#platforms-and-services)
  - [Reference and tooling](#reference-and-tooling)
  - [Directories](#directories)
- [Agent frameworks](#agent-frameworks)
  - [Python](#python)
  - [TypeScript](#typescript)
  - [Declarative](#declarative)
- [Agent infrastructure](#agent-infrastructure)
  - [Gateways and proxies](#gateways-and-proxies)
  - [Observability](#observability)
  - [Sandboxes and browsers](#sandboxes-and-browsers)
  - [Web data](#web-data)
  - [Evals](#evals)
  - [Memory](#memory)
- [Local models](#local-models)
  - [Runners](#runners)
  - [Desktop and chat UIs](#desktop-and-chat-uis)

## Coding agents

Agents that read, write and run code in your repository.

### Terminal agents

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #004 | [opencode](https://opencode.ai) | Open-source terminal coding agent that works with many model providers. | MIT | [★ 222.2k](https://github.com/anomalyco/opencode) | today |
| #001 | [Claude Code](https://www.anthropic.com/claude-code) | Anthropic's agentic coding CLI; also runs in IDEs and the desktop app. | Proprietary | [★ 153.5k](https://github.com/anthropics/claude-code) | today |
| #002 | [Codex CLI](https://developers.openai.com/codex) | OpenAI's open-source coding agent for the terminal. | Apache-2.0 | [★ 131.1k](https://github.com/openai/codex) | today |
| #003 | [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google's open-source agent that brings Gemini models to the terminal. | Apache-2.0 | [★ 108.6k](https://github.com/google-gemini/gemini-cli) | today |
| #073 | [Warp](https://www.warp.dev) | Terminal-based development environment with built-in coding agents. | AGPL-3.0 | [★ 65.7k](https://github.com/warpdotdev/warp) | today |
| #008 | [Goose](https://github.com/aaif-goose/goose) | Extensible open-source agent with a CLI and desktop app, built on MCP. | Apache-2.0 | [★ 55.8k](https://github.com/aaif-goose/goose) | today |
| #005 | [Aider](https://aider.chat) | Pair programming in the terminal with git-native edits and commits. | Apache-2.0 | [★ 49.8k](https://github.com/Aider-AI/aider) | 5mo ago |
| #006 | [Crush](https://github.com/charmbracelet/crush) | Charm's terminal coding agent with multi-model and LSP support. | FSL-1.1-MIT | [★ 28.8k](https://github.com/charmbracelet/crush) | today |
| #007 | [Qwen Code](https://github.com/QwenLM/qwen-code) | Terminal agent tuned for Qwen coder models, forked from Gemini CLI. | Apache-2.0 | [★ 28.7k](https://github.com/QwenLM/qwen-code) | today |
| #071 | [GitHub Copilot CLI](https://github.com/github/copilot-cli) | GitHub's Copilot coding agent in the terminal. | Proprietary | [★ 11.3k](https://github.com/github/copilot-cli) | today |
| #009 | [Amp](https://ampcode.com) | Sourcegraph's coding agent for the terminal and editors. | Closed source | — | — |
| #072 | [Factory](https://factory.com/) | Runs coding agents called Droids from the terminal, IDE and CI. | Closed source | — | — |

### Editor agents

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #016 | [Zed](https://zed.dev) | High-performance editor written in Rust with a built-in agent panel. | GPL-3.0 / Apache-2.0 | [★ 92.3k](https://github.com/zed-industries/zed) | today |
| #012 | [Cline](https://cline.bot) | Open-source autonomous coding agent as a VS Code extension. | Apache-2.0 | [★ 70.9k](https://github.com/cline/cline) | today |
| #015 | [Continue](https://continue.dev) | Open-source agents and checks for IDEs and CI. | Apache-2.0 | [★ 36.3k](https://github.com/continuedev/continue) | today |
| #076 | [Tabby](https://www.tabbyml.com) | Self-hosted, open-source alternative to GitHub Copilot. | Apache-2.0 + enterprise | [★ 33.9k](https://github.com/TabbyML/tabby) | 3mo ago |
| #013 | [Kilo Code](https://kilocode.ai) | Open-source agent extension for VS Code and JetBrains. | MIT | [★ 27.8k](https://github.com/Kilo-Org/kilocode) | today |
| #014 | [Roo Code](https://github.com/RooCodeInc/Roo-Code) | Multi-mode coding agent extension for VS Code, forked from Cline. | Apache-2.0 | [★ 24.3k](https://github.com/RooCodeInc/Roo-Code) | 5mo ago · 🗄️ archived |
| #074 | [Junie](https://junie.jetbrains.com/) | JetBrains' coding agent for its IDEs, the terminal and CI. | Proprietary | [★ 500](https://github.com/JetBrains/junie) | today |
| #010 | [Cursor](https://cursor.com) | AI-first fork of VS Code with an agent mode and background agents. | Closed source | — | — |
| #011 | [GitHub Copilot](https://github.com/features/copilot) | GitHub's assistant with agent mode in the editor and a cloud coding agent. | Closed source | — | — |
| #017 | [Kiro](https://kiro.dev) | AWS's agentic IDE built around specs and hooks. | Closed source | — | — |
| #075 | [Trae](https://www.trae.ai) | ByteDance's AI IDE with a built-in coding agent. | Closed source | — | — |

### Cloud and autonomous agents

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #018 | [OpenHands](https://github.com/OpenHands/OpenHands) | Open platform for autonomous software-engineering agents. | MIT | [★ 92k](https://github.com/OpenHands/OpenHands) | today |
| #019 | [SWE-agent](https://swe-agent.com) | Princeton/Stanford research agent that resolves GitHub issues. | MIT | [★ 20.6k](https://github.com/SWE-agent/SWE-agent) | today |
| #020 | [Devin](https://devin.ai) ☁️ | Cognition's autonomous software engineer. | Closed source | — | — |
| #021 | [Jules](https://jules.google) ☁️ | Google's asynchronous coding agent that works on your GitHub repos. | Closed source | — | — |
| #078 | [Tempo](https://www.tempo.new) ☁️ | Turns customer feedback, issues and product requirements into reviewed pull requests. | Closed source | — | — |

### Code review

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #077 | [CodeRabbit](https://www.coderabbit.ai) ☁️ | Reviews pull requests with AI and leaves line-by-line comments. | Closed source | — | — |

## App builders

Describe an app in plain language and get a running one back.

### Hosted

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #022 | [Lovable](https://lovable.dev) ☁️ | Builds full-stack web apps from chat, with Supabase and GitHub sync. | Closed source | — | — |
| #023 | [Bolt.new](https://bolt.new) ☁️ | StackBlitz's in-browser app builder running on WebContainers. | Closed source | — | — |
| #024 | [v0](https://v0.app) ☁️ | Vercel's generator for React and Next.js apps and UI. | Closed source | — | — |
| #025 | [Replit Agent](https://replit.com) ☁️ | Agent that builds and deploys apps inside Replit's cloud workspace. | Closed source | — | — |
| #026 | [Base44](https://base44.com) ☁️ | All-in-one builder with hosting, database and auth included. | Closed source | — | — |
| #027 | [Firebase Studio](https://firebase.studio) ☁️ | Google's cloud workspace for prototyping and shipping full-stack apps. | Closed source | — | — |
| #079 | [Anything](https://www.anything.com) ☁️ | Builds websites, apps and tools from a text description. | Closed source | — | — |
| #080 | [Rork](https://rork.com) ☁️ | Builds cross-platform mobile apps from a prompt. | Closed source | — | — |
| #081 | [Leap](https://leap.new) ☁️ | Generates apps and deploys them to AWS or GCP. | Closed source | — | — |

### Open source and local

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #083 | [Onlook](https://www.onlook.com/) | Visual editor for React apps that writes design changes back to the code. | Apache-2.0 | [★ 27k](https://github.com/onlook-dev/onlook) | 6d ago |
| #028 | [Dyad](https://www.dyad.sh) | Local, open-source alternative to hosted app builders. | Apache-2.0 + pro | [★ 22.1k](https://github.com/dyad-sh/dyad) | today |
| #029 | [bolt.diy](https://github.com/stackblitz-labs/bolt.diy) | Community fork of Bolt.new that runs with any LLM provider. | MIT | [★ 20k](https://github.com/stackblitz-labs/bolt.diy) | 13d ago |
| #082 | [Chef](https://github.com/get-convex/chef) | Convex's open-source app builder that generates the backend along with the UI. | Apache-2.0 | [★ 4.6k](https://github.com/convex/chef) | 13d ago |

## MCP servers

Model Context Protocol servers that give agents tools and data.

### Developer tools

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #033 | [Context7](https://context7.com) | Up-to-date, version-specific library docs fed into the prompt. | MIT | [★ 63.8k](https://github.com/upstash/context7) | today |
| #032 | [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Lets agents drive and debug a live Chrome via DevTools. | Apache-2.0 | [★ 54.2k](https://github.com/ChromeDevTools/chrome-devtools-mcp) | today |
| #031 | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Browser automation through Playwright's accessibility snapshots. | Apache-2.0 | [★ 38.7k](https://github.com/microsoft/playwright-mcp) | 5d ago |
| #030 | [GitHub MCP Server](https://github.com/github/github-mcp-server) | GitHub's official server for repos, issues, PRs and Actions. | MIT | [★ 34k](https://github.com/github/github-mcp-server) | 4d ago |
| #087 | [Serena](https://oraios.github.io/serena/) | Gives coding agents semantic code search and editing through language servers. | GPL-3.0 / MIT | [★ 30.8k](https://github.com/oraios/serena) | today |
| #088 | [Desktop Commander](https://desktopcommander.app/) | Gives MCP clients terminal control, file search and diff-based file editing. | MIT | [★ 10.1k](https://github.com/wonderwhy-er/DesktopCommanderMCP) | today |
| #085 | [Firecrawl MCP](https://github.com/firecrawl/firecrawl-mcp-server) | Adds Firecrawl web scraping, crawling and search to MCP clients. | MIT | [★ 7.7k](https://github.com/firecrawl/firecrawl-mcp-server) | today |
| #086 | [Exa MCP](https://exa.ai/docs/get-started/exa-mcp) | Connects MCP clients to Exa's web search and page fetching. | MIT | [★ 5.2k](https://github.com/exa-labs/exa-mcp-server) | 8d ago |

### Platforms and services

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #037 | [AWS MCP Servers](https://github.com/awslabs/mcp) | AWS Labs' collection of servers for AWS services. | Apache-2.0 | [★ 9.8k](https://github.com/awslabs/mcp) | today |
| #035 | [Notion MCP Server](https://github.com/makenotion/notion-mcp-server) | Notion's official server for pages and databases. | MIT | [★ 4.7k](https://github.com/makenotion/notion-mcp-server) | 1mo ago |
| #084 | [Cloudflare MCP](https://github.com/cloudflare/mcp-server-cloudflare) | Cloudflare's MCP servers for Workers, DNS, observability and other Cloudflare APIs. | Apache-2.0 | [★ 4.4k](https://github.com/cloudflare/mcp-server-cloudflare) | 5d ago |
| #091 | [Microsoft MCP](https://github.com/microsoft/mcp) | Catalog of Microsoft's official MCP servers, including Azure. | MIT | [★ 3.8k](https://github.com/microsoft/mcp) | today |
| #089 | [Grafana MCP](https://github.com/grafana/mcp-grafana) | Grafana's MCP server for querying dashboards, data sources and alerts. | Apache-2.0 | [★ 3.6k](https://github.com/grafana/mcp-grafana) | today |
| #034 | [Supabase MCP](https://github.com/supabase/mcp) | Manage Supabase projects, databases and edge functions. | Apache-2.0 | [★ 3k](https://github.com/supabase/mcp) | today |
| #036 | [Stripe](https://github.com/stripe/ai) | Stripe's agent toolkit and MCP server for payments APIs. | MIT | [★ 2k](https://github.com/stripe/ai) | today |
| #090 | [MongoDB MCP Server](https://github.com/mongodb-js/mongodb-mcp-server) | Connects agents to MongoDB databases and Atlas clusters. | Apache-2.0 | [★ 1.1k](https://github.com/mongodb-js/mongodb-mcp-server) | today |

### Reference and tooling

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #038 | [Reference servers](https://github.com/modelcontextprotocol/servers) | Official reference implementations (filesystem, fetch, git, memory...). | Apache-2.0 / MIT | [★ 91.6k](https://github.com/modelcontextprotocol/servers) | today |
| #092 | [FastMCP](https://gofastmcp.com/getting-started/welcome) | Builds MCP servers and clients in Python with a decorator-based API. | Apache-2.0 | [★ 28.2k](https://github.com/PrefectHQ/fastmcp) | today |
| #094 | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | Official Python SDK for building MCP servers and clients. | MIT | [★ 24.7k](https://github.com/modelcontextprotocol/python-sdk) | today |
| #093 | [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) | Official TypeScript SDK for building MCP servers and clients. | Apache-2.0 / MIT | [★ 13.7k](https://github.com/modelcontextprotocol/typescript-sdk) | today |
| #039 | [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Visual tool for testing and debugging MCP servers. | Apache-2.0 / MIT | [★ 11.2k](https://github.com/modelcontextprotocol/inspector) | 2d ago |
| #095 | [MCP Registry](https://github.com/modelcontextprotocol/registry) | Official community-driven registry service for MCP servers. | Apache-2.0 / MIT | [★ 7.4k](https://github.com/modelcontextprotocol/registry) | today |

### Directories

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #042 | [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | The largest community list of MCP servers. | MIT | [★ 96.9k](https://github.com/punkpeye/awesome-mcp-servers) | 4d ago |
| #040 | [Smithery](https://smithery.ai) ☁️ | Registry for discovering and hosting MCP servers. | Closed source | — | — |
| #041 | [Glama](https://glama.ai/mcp/servers) ☁️ | Searchable directory of MCP servers. | Closed source | — | — |

## Agent frameworks

Libraries and SDKs for building your own agents.

### Python

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #064 | [AutoGen](https://microsoft.github.io/autogen/) | Microsoft's framework for building multi-agent conversational AI applications. | CC-BY-4.0 | [★ 61.6k](https://github.com/microsoft/autogen) | 11d ago |
| #060 | [CrewAI](https://crewai.com/) | Orchestrates teams of role-playing autonomous agents in Python. | MIT | [★ 60.2k](https://github.com/crewAIInc/crewAI) | today |
| #067 | [LlamaIndex](https://www.llamaindex.ai) | Builds agents and RAG pipelines over private documents and data. | MIT | [★ 52.7k](https://github.com/run-llama/llama_index) | today |
| #059 | [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) | Builds stateful, long-running agents as graphs, from the LangChain team. | MIT | [★ 44k](https://github.com/langchain-ai/langgraph) | today |
| #068 | [DSPy](https://dspy.ai) | Programs language models with composable modules and optimizers instead of hand-written prompts. | MIT | [★ 38.8k](https://github.com/stanfordnlp/dspy) | today |
| #061 | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | OpenAI's lightweight Python framework for multi-agent workflows with handoffs and guardrails. | MIT | [★ 30.3k](https://github.com/openai/openai-agents-python) | today |
| #066 | [smolagents](https://huggingface.co/docs/smolagents/index) | Hugging Face's minimal library for agents that act by writing code. | Apache-2.0 | [★ 30.1k](https://github.com/huggingface/smolagents) | 5d ago |
| #065 | [Google ADK](https://adk.dev/) | Google's toolkit for building, evaluating and deploying agents in Python. | Apache-2.0 | [★ 22k](https://github.com/google/adk-python) | today |
| #063 | [Pydantic AI](https://pydantic.dev/pydantic-ai) | Builds type-safe agents in Python, from the team behind Pydantic. | MIT | [★ 20.9k](https://github.com/pydantic/pydantic-ai) | today |
| #062 | [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python) | Builds agents in Python on the same agent harness that powers Claude Code. | MIT | [★ 8.4k](https://github.com/anthropics/claude-agent-sdk-python) | today |

### TypeScript

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #070 | [Mastra](https://mastra.ai) | TypeScript framework for agents, workflows, RAG and evals. | Apache-2.0 + enterprise | [★ 29.1k](https://github.com/mastra-ai/mastra) | today |
| #069 | [Vercel AI SDK](https://github.com/vercel/ai) | TypeScript toolkit for building AI apps and agents across model providers. | Apache-2.0 | [★ 27.5k](https://github.com/vercel/ai) | today |

### Declarative

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #107 | [Docker Agent](https://github.com/docker/docker-agent) | Docker's CLI plugin for building and running multi-agent teams defined in YAML. | Apache-2.0 | [★ 4.6k](https://github.com/docker/docker-agent) | today |

## Agent infrastructure

Gateways, observability and sandboxes for running agents in production.

### Gateways and proxies

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #043 | [LiteLLM](https://github.com/BerriAI/litellm) | Python SDK and proxy that calls 100+ LLM APIs in OpenAI format. | MIT + enterprise | [★ 62.1k](https://github.com/BerriAI/litellm) | today |
| #106 | [magpie](https://usemagpie.ai) | Local gateway that lets Claude Code, Codex and other agents use any model, from the menu bar. | MIT | [★ 23.3k](https://github.com/yetone/magpie) | today |
| #044 | [Portkey Gateway](https://github.com/Portkey-AI/gateway) | Fast AI gateway with routing, retries and guardrails. | MIT | [★ 13.3k](https://github.com/Portkey-AI/gateway) | 5mo ago |
| #045 | [omni](https://github.com/ergonlabs-io/omni) ¹ | One interception point for all coding agents. | MIT | [★ 0](https://github.com/ergonlabs-io/omni) | 1mo ago |
| #096 | [OpenRouter](https://openrouter.ai) ☁️ | Routes requests to hundreds of models from many providers through one OpenAI-compatible API. | Closed source | — | — |

### Observability

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #046 | [Langfuse](https://langfuse.com) | Open-source LLM tracing, evals and prompt management. | MIT + enterprise | [★ 36.6k](https://github.com/langfuse/langfuse) | today |
| #098 | [Opik](https://www.comet.com/docs/opik/) | Comet's open-source tracing, evaluation and monitoring for LLM apps. | Apache-2.0 | [★ 23k](https://github.com/comet-ml/opik) | today |
| #097 | [Arize Phoenix](https://arize.com/phoenix/) | Traces, evaluates and debugs LLM apps and agents, built on OpenTelemetry. | Elastic-2.0 | [★ 12k](https://github.com/Arize-ai/phoenix) | today |
| #047 | [Helicone](https://helicone.ai) | Open-source LLM observability and gateway. | Apache-2.0 | [★ 6.2k](https://github.com/Helicone/helicone) | 3d ago |

### Sandboxes and browsers

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #049 | [Browser Use](https://browser-use.com) | Makes websites accessible to AI agents. | MIT | [★ 119.3k](https://github.com/browser-use/browser-use) | today |
| #099 | [Stagehand](https://www.stagehand.dev/) | Browser automation SDK that mixes code with natural-language actions. | MIT | [★ 25.8k](https://github.com/browserbase/stagehand) | today |
| #048 | [E2B](https://e2b.dev) | Secure cloud sandboxes for running agent-generated code. | Apache-2.0 | [★ 14.6k](https://github.com/e2b-dev/E2B) | today |
| #100 | [Browserbase](https://www.browserbase.com) ☁️ | Runs headless browsers in the cloud for agents and automation. | Closed source | — | — |

### Web data

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #101 | [Firecrawl](https://www.firecrawl.dev) | Turns websites into clean Markdown or structured data for LLMs through an API. | AGPL-3.0 | [★ 195.9k](https://github.com/firecrawl/firecrawl) | today |
| #102 | [Crawl4AI](https://crawl4ai.com) | Open-source crawler that turns web pages into clean Markdown or JSON for LLMs. | Apache-2.0 | [★ 86.4k](https://github.com/unclecode/crawl4ai) | today |

### Evals

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #103 | [promptfoo](https://www.promptfoo.dev) | Tests and red-teams prompts, agents and RAG pipelines from the CLI or CI. | MIT | [★ 26.5k](https://github.com/promptfoo/promptfoo) | today |

### Memory

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #104 | [Mem0](https://mem0.ai) | Adds a persistent memory layer so agents recall past interactions. | Apache-2.0 | [★ 67.9k](https://github.com/mem0ai/mem0) | today |
| #105 | [Letta](https://www.letta.com) | Builds stateful agents with long-term memory, from the team behind MemGPT. | Apache-2.0 | [★ 25.3k](https://github.com/letta-ai/letta) | 9d ago |

## Local models

Run open-weight models on your own hardware.

### Runners

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #050 | [Ollama](https://ollama.com) | Runs open-weight models locally behind a simple CLI and an OpenAI-compatible API. | MIT | [★ 185k](https://github.com/ollama/ollama) | today |
| #051 | [llama.cpp](https://llama.app) | Runs LLM inference in plain C/C++ on CPUs and GPUs; the engine behind many local tools. | MIT | [★ 132.5k](https://github.com/ggml-org/llama.cpp) | today |
| #052 | [vLLM](https://vllm.ai) | Serves LLMs with high throughput using PagedAttention and continuous batching. | Apache-2.0 | [★ 95.7k](https://github.com/vllm-project/vllm) | today |
| #055 | [LocalAI](https://localai.io) | Serves LLM, vision, voice and image models on local hardware through an OpenAI-compatible API. | MIT | [★ 50k](https://github.com/mudler/LocalAI) | today |
| #053 | [SGLang](https://www.sglang.io/) | Serves LLMs and multimodal models with a fast runtime and a structured-generation frontend. | Apache-2.0 | [★ 38.3k](https://github.com/sgl-project/sglang) | today |
| #054 | [MLX LM](https://github.com/ml-explore/mlx-lm) | Runs and fine-tunes LLMs on Apple silicon with Apple's MLX framework. | MIT | [★ 7.5k](https://github.com/ml-explore/mlx-lm) | 3d ago |

### Desktop and chat UIs

| # | Tool | What it does | License | Stars | Last commit |
| --- | --- | --- | --- | --- | --- |
| #058 | [Open WebUI](https://openwebui.com) | Self-hosted chat interface for Ollama and OpenAI-compatible APIs. | Custom (Open WebUI License) | [★ 156.9k](https://github.com/open-webui/open-webui) | today |
| #057 | [Jan](https://www.jan.ai/) | Runs an offline, open-source ChatGPT-style assistant on local models or cloud APIs. | Apache-2.0 | [★ 45.1k](https://github.com/janhq/jan) | today |
| #056 | [LM Studio](https://lmstudio.ai) | Desktop app for finding, downloading and chatting with local models, with a local API server. | Closed source | — | — |

---

"+ enterprise" / "+ pro" in the License column: open core, with some directories under a commercial license.

¹ Built by [Ergonlabs](https://ergonlabs.io), which maintains this list. It is held to the same inclusion rules as every other entry.

Generated by `scripts/build.py` from [`data/`](data/). Edit the YAML, not this file.
