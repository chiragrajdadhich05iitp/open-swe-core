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
