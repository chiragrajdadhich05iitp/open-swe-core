🖥️ Running Locally
Open two terminal tabs to run both backend and frontend concurrently:

Terminal 1: LangGraph Backend Server
PowerShell
uv run langgraph dev --allow-blocking
Runs the local execution engine and LangGraph API endpoint (default: http://127.0.0.1:2024).

Terminal 2: Agent Dashboard Web UI
PowerShell
pnpm dev
Launches the interactive web console at http://localhost:3000.

🧪 Verified Workflow & Example Run
The setup includes verified local verification cycles:

Task Planning: Deconstructs user specifications into concrete code modifications.

File Generation: Writes clean, typed code directly into the workspace root.

Automated Verification: Automatically writes test suites and executes them with test runners (e.g., TestClient, pytest) before presenting the solution.

Plaintext
Prompt: "Create a FastAPI server in app.py with a /health route and test it."
Result: 
  ✔ Created app.py with FastAPI /health endpoint
  ✔ Verified with TestClient (Status HTTP 200, {"status": "healthy"})
👤 Author & Maintainer
Chirag Dah

Built & Configured with Open-SWE, LangGraph & modern LLM toolchains.

📄 License
This project is licensed under the terms specified in the LICENSE file.
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("README.md generated successfully.")


```text?code_stdout&code_event_index=1
README.md generated successfully.

Your Markdown file is ready
[file-tag: code-generated-file-81b46ddb-3bd4-4308-9d61-6143fe6e1a1d]

File Content Preview:
Markdown
# Open-SWE: Autonomous Asynchronous Coding Agent 🚀

An autonomous software engineering agent built on top of **LangGraph**, **LangSmith**, and modern asynchronous Python runtime environments. Open-SWE is designed to plan, edit, execute, and verify codebases autonomously within sandboxed developer environments.

---

## 🌟 Highlights & Architecture

- **Graph-Driven Execution**: Orchestrated using **LangGraph** workflows with explicit human-in-the-loop and verification cycles.
- **Deep Observability**: Out-of-the-box support for **LangSmith Studio** for real-time state tracking, trace debugging, and run analytics.
- **Asynchronous & Non-Blocking**: High-throughput task queues powered by Python's `asyncio` loop with dev-mode blocking bypass (`--allow-blocking`).
- **Modern Dev Toolchain**: Built with high-speed toolchains:
  - **uv** for blazing fast Python virtual environments and dependency management.
  - **pnpm** and **Vite** for the reactive frontend dashboard.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, LangGraph, LangGraph CLI, LangChain, FastAPI, Uvicorn
- **Frontend Dashboard**: Vite, React, TanStack Router, TanStack Query
- **Package Managers**: `uv` (Python), `pnpm` (Node/TypeScript)
- **Supported LLMs**: OpenAI (GPT-4o, o-series), Anthropic (Claude 3.5 Sonnet)

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have the following installed:
- [Python 3.11+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (`pip install uv` or via standalone installer)
- [Node.js](https://nodejs.org/) & [pnpm](https://pnpm.io/) (`npm install -g pnpm`)

### 2. Installation & Environment Setup

Clone the repository and set up dependencies:

```bash
# Clone the repository
git clone [https://github.com/](https://github.com/)<your-username>/open-swe.git
cd open-swe

# Install Python dependencies with uv
uv sync

# Install frontend UI dependencies
pnpm install
3. Environment Variables
Create a .env file in the root directory:

Code snippet
# LangSmith Observability
LANGSMITH_API_KEY=your_langsmith_key_here
LANGCHAIN_TRACING_V2=true

# Model Providers
OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
🖥️ Running Locally
Open two terminal tabs to run both backend and frontend concurrently:

Terminal 1: LangGraph Backend Server
PowerShell
uv run langgraph dev --allow-blocking
Runs the local execution engine and LangGraph API endpoint (default: http://127.0.0.1:2024).

Terminal 2: Agent Dashboard Web UI
PowerShell
pnpm dev
Launches the interactive web console at http://localhost:3000.

🧪 Verified Workflow & Example Run
The setup includes verified local verification cycles:

Task Planning: Deconstructs user specifications into concrete code modifications.

File Generation: Writes clean, typed code directly into the workspace root.

Automated Verification: Automatically writes test suites and executes them with test runners (e.g., TestClient, pytest) before presenting the solution.

Plaintext
Prompt: "Create a FastAPI server in app.py with a /health route and test it."
Result: 
  ✔ Created app.py with FastAPI /health endpoint
  ✔ Verified with TestClient (Status HTTP 200, {"status": "healthy"})
👤 Author & Maintainer
Chirag Raj Dadhich

Built & Configured with Open-SWE, LangGraph & modern LLM toolchains.

📄 License
This project is licensed under the terms specified in the LICENSE file.