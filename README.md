# 🎮 Multi-Agent Game Dev Assistant
A fully automated game development system powered by multi-agent collaboration, built with AutoGen.

---

## ✨ Overview
This project leverages the power of multi-agent collaboration to automate the entire game development workflow. From a simple text prompt like "create a classic Snake game," the system orchestrates specialized AI agents to handle planning, design, coding, testing, and debugging.

It's built on the AutoGen framework and uses the Tongyi Qwen LLM, demonstrating the practical application of AI agents in software engineering.

---

## 🧠 Core Architecture
The system is composed of multiple specialized agents, each with a dedicated role:

| Agent | Role & Responsibility |
| :--- | :--- |
| 📝 Planner Agent | Breaks down the user's request into a clear, actionable game design document and technical plan. |
| 🎨 Artist Agent | Defines the game's visual style, character design, and UI elements, providing creative direction. |
| 💻 Programmer Agent | Writes clean, modular, and runnable Pygame code based on the plan and design. |
| 🧪 Tester Agent | Runs the generated code, identifies bugs and logical errors, and provides detailed feedback for fixes. |
| 🔧 Tool Integration | Agents can use tools for file management, code execution, and version control to complete tasks. |

---

## 🚀 Features
- End-to-End Automation: Generates complete, runnable games from natural language prompts.
- RAG-Enhanced Generation: Uses a Chroma vector database to store game development knowledge, improving code accuracy and reducing hallucinations.
- Modular & Extensible: The agent-based design makes it easy to add new roles or swap out the underlying LLM.
- Full Engineering Pipeline: Includes logging, error handling, and a structured project layout for production readiness.

---

## 🛠️ Tech Stack
- Language: Python 3.9+
- Framework: AutoGen / AutoGen-Core
- LLM: Tongyi Qwen (Alibaba Cloud)
- Libraries: Pygame, Chroma DB, python-dotenv

---

## 📂 Project Structure
AutoGen_project/
├── agents/             # Definitions for all agents
├── config/             # LLM and project settings
├── rag/                # Retrieval-Augmented Generation components
├── tools/              # Utility tools (file manager, logger, etc.)
├── main.py             # The main entry point
└── .env                # API keys (keep this file private!)

---

## ⚙️ Setup & Run
1. Clone the repository
git clone https://github.com/haohaobetter/multi-agent-game-dev-assistant.git
cd multi-agent-game-dev-assistant

2. Install dependencies
pip install -r requirements.txt

3. Configure your .env file
Create a .env file in the root directory and add your API keys:
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=your_base_url_here

4. Run the assistant
python main.py

---

## 📌 Note
This is a personal project for learning and demonstrating multi-agent systems. 