# Open-SWE Core: Autonomous Asynchronous Coding Agent ⚡

An asynchronous, graph-orchestrated software engineering agent environment designed to plan, generate, execute, and verify code within isolated developer workspaces. Built with a focus on deep observability, test-driven validation, and seamless human-in-the-loop interaction.

---

## 🌟 Architecture & Key Capabilities

- **Graph-Driven Workflow**: Stateful task orchestration powered by **LangGraph**, enabling cyclical execution, automated error recovery, and structured planning.
- **Deep Observability & Tracing**: Real-time run tracking, prompt inspection, and token analytics integrated natively with **LangSmith**.
- **Dual-Engine Execution**: Asynchronous task scheduling with non-blocking event loops (`--allow-blocking` dev runtime support).
- **Automated Verification Loop**: Generates targeted tests (e.g., via `TestClient`, `pytest`) and verifies output correctness before presenting code changes.
- **Modern Dev Toolchain**: Fully isolated Python runtime managed with **uv** and a reactive Vite/React developer dashboard managed with **pnpm**.

---

## 🛠️ System Architecture & Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Agent Orchestration** | LangGraph, LangChain, Python 3.12+ (asyncio) |
| **Observability & Eval** | LangSmith Studio, OpenTelemetry |
| **Frontend Console** | React, Vite, TanStack Router, TanStack Query |
| **Environment Tooling**| `uv` (Fast Python package manager), `pnpm` |
| **Supported LLMs** | OpenAI (GPT-4o, o-series), Anthropic (Claude 3.5 Sonnet) |

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the following installed locally:
- **Python 3.11+**
- [uv](https://docs.astral.sh/uv/) for Python package management
- [Node.js](https://nodejs.org/) & [pnpm](https://pnpm.io/) for the dashboard UI

### 2. Installation

Clone the repository and set up the local environment:

```bash
# Clone the repository
git clone [https://github.com/chiragrajdadhich05iitp/open-swe-core.git](https://github.com/chiragrajdadhich05iitp/open-swe-core.git)
cd open-swe-core

# Sync Python virtual environment & dependencies
uv sync

# Install frontend dependencies
pnpm install

🖥️ Running Locally
Run both the orchestration backend and web console using two terminal sessions:

Terminal 1: LangGraph Backend Engine
PowerShell
uv run langgraph dev --allow-blocking
Initializes the local execution server and agent endpoints (accessible at http://127.0.0.1:2024).

Terminal 2: Developer Dashboard UI
PowerShell
pnpm dev
Spins up the web console at http://localhost:3000 for task submission and code diff review.

🧪 Verified Execution Sample
The agent pipeline has been verified with end-to-end task generation and test execution:

Plaintext
User Request: 
"Create a FastAPI server in app.py with a /health route and test it."

Agent Action Pipeline:
  1. Planned endpoint signature and health-check schema.
  2. Generated app.py with FastAPI route returning {"status": "healthy"}.
  3. Formulated and executed automated test script via FastAPI TestClient.
  4. Confirmed HTTP 200 and schema validity before staging changes.
📌 Implementation & System Engineering
Maintained & Engineered by: Chirag Raj Dadhich

Focus: Agentic AI Orchestration, Asynchronous Workflows, and Developer Tooling.

📄 License
This project is distributed under the terms of the LICENSE included in this repository.
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("Professional README ready.")


```text?code_stdout&code_event_index=1
Professional README ready.

Your Markdown file is ready
[file-tag: code-generated-file-0809dcb8-e98e-44bc-8f81-78029c0f8d55]

GitHub repository ke liye professional, clean aur technically solid README:

Markdown
# Open-SWE Core: Autonomous Asynchronous Coding Agent ⚡

An asynchronous, graph-orchestrated software engineering agent environment designed to plan, generate, execute, and verify code within isolated developer workspaces. Built with a focus on deep observability, test-driven validation, and seamless human-in-the-loop interaction.

---

## 🌟 Architecture & Key Capabilities

- **Graph-Driven Workflow**: Stateful task orchestration powered by **LangGraph**, enabling cyclical execution, automated error recovery, and structured planning.
- **Deep Observability & Tracing**: Real-time run tracking, prompt inspection, and token analytics integrated natively with **LangSmith**.
- **Dual-Engine Execution**: Asynchronous task scheduling with non-blocking event loops (`--allow-blocking` dev runtime support).
- **Automated Verification Loop**: Generates targeted tests (e.g., via `TestClient`, `pytest`) and verifies output correctness before presenting code changes.
- **Modern Dev Toolchain**: Fully isolated Python runtime managed with **uv** and a reactive Vite/React developer dashboard managed with **pnpm**.

---

## 🛠️ System Architecture & Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Agent Orchestration** | LangGraph, LangChain, Python 3.12+ (asyncio) |
| **Observability & Eval** | LangSmith Studio, OpenTelemetry |
| **Frontend Console** | React, Vite, TanStack Router, TanStack Query |
| **Environment Tooling**| `uv` (Fast Python package manager), `pnpm` |
| **Supported LLMs** | OpenAI (GPT-4o, o-series), Anthropic (Claude 3.5 Sonnet) |

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the following installed locally:
- **Python 3.11+**
- [uv](https://docs.astral.sh/uv/) for Python package management
- [Node.js](https://nodejs.org/) & [pnpm](https://pnpm.io/) for the dashboard UI

### 2. Installation

Clone the repository and set up the local environment:

```bash
# Clone the repository
git clone [https://github.com/chiragrajdadhich05iitp/open-swe-core.git](https://github.com/chiragrajdadhich05iitp/open-swe-core.git)
cd open-swe-core

# Sync Python virtual environment & dependencies
uv sync

# Install frontend dependencies
pnpm install
3. Configuration
Configure your environment variables in a .env file at the root:

Code snippet
# LangSmith Tracing & Observability
LANGSMITH_API_KEY=your_langsmith_key_here
LANGCHAIN_TRACING_V2=true

# Model Providers (Set at least one)
OPENAI_API_KEY=sk-proj-...
# ANTHROPIC_API_KEY=sk-ant-...
🖥️ Running Locally
Run both the orchestration backend and web console using two terminal sessions:

Terminal 1: LangGraph Backend Engine
PowerShell
uv run langgraph dev --allow-blocking
Initializes the local execution server and agent endpoints (accessible at http://127.0.0.1:2024).

Terminal 2: Developer Dashboard UI
PowerShell
pnpm dev
Spins up the web console at http://localhost:3000 for task submission and code diff review.

🧪 Verified Execution Sample
The agent pipeline has been verified with end-to-end task generation and test execution:

Plaintext
User Request: 
"Create a FastAPI server in app.py with a /health route and test it."

Agent Action Pipeline:
  1. Planned endpoint signature and health-check schema.
  2. Generated app.py with FastAPI route returning {"status": "healthy"}.
  3. Formulated and executed automated test script via FastAPI TestClient.
  4. Confirmed HTTP 200 and schema validity before staging changes.
📌 Implementation & System Engineering
Maintained & Engineered by: Chirag Raj Dadhich

Focus: Agentic AI Orchestration, Asynchronous Workflows, and Developer Tooling.

📄 License
This project is distributed under the terms of the LICENSE included in this repository.
