# 🧠 TerminalMind

> **An AI-powered Windows terminal assistant — talk to your system in plain English.**

TerminalMind lets you skip memorizing commands. Ask *"What's my IP?"* or *"Show me running processes"* and the AI decides which tool to run, executes it, and explains the results conversationally.

---

## ✨ Features

- 🤖 **Natural Language Interface** — Describe what you want, no command memorization needed
- ⚙️ **16 Built-in System Tools** — Network diagnostics, system info, processes, disk usage, and more
- 🧪 **AI/ML Integration** — Run Isolation Forest anomaly detection on your CSV data via file dialogs
- 💬 **Persistent Session Memory** — Remembers context across your entire session
- 🎨 **Beautiful Terminal UI** — Spinners, markdown rendering, colored panels, and ASCII art banner

---

## 🗂️ Project Structure

```
terminalmind/                  ← Project root
│
├── .env                       ← Your API key (YOU create this, never committed)
├── .gitignore
├── README.md
├── requirements.txt           ← All dependencies with pinned versions
├── setup.py                   ← Package config + entry point
│
└── terminalmind/              ← Python package
    ├── __init__.py
    └── main.py                ← Entire application
```

---

## 🚀 Setup Guide

### Prerequisites

- **Windows 10/11**
- **Python 3.8+** → [python.org/downloads](https://www.python.org/downloads/)
- **A Groq API key** → [console.groq.com](https://console.groq.com) (free)

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/your-username/terminalmind.git
cd terminalmind
```

---

### Step 2 — Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

You'll see `(venv)` appear in your terminal prompt confirming activation.

---

### Step 3 — Install dependencies

**Option A** — Install packages only:
```bash
pip install -r requirements.txt
```

**Option B** — Install as a registered terminal command (recommended):
```bash
pip install -e .
```

> With Option B, you can launch the app from **any directory** just by typing `terminalmind`.

---

### Step 4 — Create your `.env` file ⚠️

> **This step is mandatory.** The `.env` file is in `.gitignore` and is **never committed to the repo** — you must create it yourself.

Create a file named `.env` in the **root of the project** (same folder as `setup.py`) with:

```env
GROQ_API_KEY="your_groq_api_key_here"
KMP_DUPLICATE_LIB_OK=TRUE
```

- `GROQ_API_KEY` — Get yours free from [console.groq.com](https://console.groq.com)
- `KMP_DUPLICATE_LIB_OK=TRUE` — Prevents an OpenMP/joblib conflict on Windows (required for anomaly detection)

> ❌ If you skip this step, the app will fail to start with an API key error.

---

### Step 5 — Run TerminalMind

```bash
# If you used Option B (pip install -e .)
terminalmind

# If you used Option A (pip install -r requirements.txt)
python terminalmind/main.py
```

The terminal will clear and the TerminalMind banner will appear. You're ready to go!

---

## 🏗️ How It Works

### Agent Pipeline

Every query goes through a two-step LLM pipeline:

```
Your Input
    │
    ▼
LLM Call #1 — reads your query + all tool descriptions
    │              decides which tool to call (or none)
    ├── No tool → respond directly
    │
    └── Tool selected
            │
            ▼
        Tool executes (subprocess / file dialog / ML model)
            │
            ▼
        Raw output shown in terminal (400 char preview)
            │
            ▼
        LLM Call #2 — summarizes the output conversationally
            │
            ▼
        Final response rendered in rich Panel (Markdown)
```

The full `chat_history` is maintained in memory across every turn so the AI has complete session context.

---

## 🛠️ Available Tools

### 🌐 Network

| Tool | Windows Command | What it does |
|------|----------------|--------------|
| `ipconfig` | `ipconfig` | IP, subnet mask, default gateway |
| `netstat` | `netstat -an` | Active connections and listening ports |
| `arp_table` | `arp -a` | IP ↔ MAC address mappings |
| `route_table` | `route print` | Routing table and gateways |
| `get_mac_addresses` | `getmac` | MAC addresses for all adapters |
| `get_hostname` | `hostname` | Computer's network hostname |
| `wifi_profiles` | `netsh wlan show profiles` | Saved Wi-Fi networks |
| `wifi_interface_info` | `netsh wlan show interfaces` | Current Wi-Fi status and signal |

### 💻 System

| Tool | Windows Command | What it does |
|------|----------------|--------------|
| `system_info` | `systeminfo` | Full OS and hardware details |
| `running_processes` | `tasklist` | All active processes |
| `disk_info` | `wmic logicaldisk get ...` | Drive sizes and free space |
| `environment_variables` | `set` | All system environment variables |

### 📁 File System

| Tool | Windows Command | What it does |
|------|----------------|--------------|
| `list_directory` | `dir` | Files and folders in current directory |
| `current_directory` | `cd` | Current working directory path |
| `system_time` | `time /t` + `date /t` | Current system date and time |

### 🤖 AI / ML

| Tool | What it does |
|------|--------------|
| `run_anomaly_inference` | Loads a pre-trained `.pkl` Isolation Forest model, runs inference on a `.csv` file, and saves `results.csv` |

**Anomaly detection flow:**
1. File dialog opens → select your `.pkl` model file
2. File dialog opens → select your `.csv` data file
3. Model loaded via `joblib`, data via `pandas`
4. Predictions run: `-1 → 1 (Anomaly)`, `1 → 0 (Normal)`
5. `results.csv` saved in the same folder as your input CSV
6. AI confirms success and tells you where the file was saved

---

## 💡 Example Interactions

```
› What's my IP address?
  ⚙  Executing ipconfig
  ✓ Command Executed  [2400 characters]
  🤖 TerminalMind: I ran ipconfig and here are your network details...

› Show me all running processes
  ⚙  Executing running_processes
  ✓ Command Executed
  🤖 TerminalMind: Here are the active processes on your system...

› Run anomaly detection on my data
  ⚙  Executing run_anomaly_inference
  Please select your .pkl model file...   [dialog opens]
  Please select your .csv data file...    [dialog opens]
  🤖 TerminalMind: Inference complete! results.csv saved to C:\Users\...

› exit
  ╔══════════════════════════════╗
  ║ Thanks for using TerminalMind║
  ║ See you next time            ║
  ╚══════════════════════════════╝
```

---

## 🧩 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `langchain` | 1.2.10 | Core LLM framework and tool abstractions |
| `langchain-core` | 1.2.18 | Tool decorator, message types |
| `langchain-groq` | 1.1.2 | Groq API integration |
| `python-dotenv` | 1.1.1 | Load API key from `.env` |
| `rich` | 13.7.1 | Terminal UI (panels, markdown, spinners) |
| `joblib` | 1.5.1 | Deserialize `.pkl` ML models |
| `numpy` | 1.26.4 | Numerical operations for inference |
| `pandas` | 2.2.2 | Read CSVs, build results DataFrames |
| `scikit-learn` | 1.2.2 | Isolation Forest model support |

`tkinter` is also used (built into Python — no install needed).

---

## ⚠️ Notes & Limitations

- **Windows only** — Tools use Windows-specific commands (`ipconfig`, `netsh`, `wmic`, `tasklist`, etc.)
- **Internet required** — The LLM runs in the cloud via Groq's API
- **Anomaly model format** — Expects a scikit-learn `IsolationForest` model saved with `joblib.dump()`. The CSV must have the same features the model was trained on (no label column)
- **Groq rate limits** — The free tier has limits; if you hit them, wait a moment and retry

---

## 🔑 Changing the LLM Model

In `terminalmind/main.py`:

```python
llm = ChatGroq(
    model="openai/gpt-oss-120b",   # ← change this
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)
```

Replace with any model available on your Groq dashboard (e.g. `llama3-70b-8192`, `mixtral-8x7b-32768`).

---

*Built with ❤️ using Python, LangChain, Groq, and Rich.*
