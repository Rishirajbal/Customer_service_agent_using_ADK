## Customer Service Agent - Project Overview

This repository contains a modular customer service agent with two runnable variants:

- CLI-only interactive app (terminal-based)
- Streamlit UI app (web-based)

Both variants reuse the same core agent package under `Project/customer_service_agent`, which defines the primary agent and specialized sub-agents, along with session/state utilities.

### Key Features
- Main agent delegates to specialized sub-agents (policy, sales, course support, order)
- In-memory session storage via `InMemorySessionService`
- Asynchronous message processing using the Google ADK runner
- Clear state management and interaction history utilities

### Project Structure
- `Project/customer_service_agent/`
  - `__init__.py`: package marker
  - `agent.py`: defines the main agent and registers sub-agents
  - `utils.py`: shared helpers for state management and agent execution
  - `tools/`: specialized sub-agents
    - `policy_agent/agent.py`
    - `sales_agent/agent.py`
    - `course_support_agent/agent.py`
    - `order_agent/agent.py`
- `Project/README_CLI.md`: CLI-only setup and usage
- `Project/README_Streamlit.md`: Streamlit setup and usage
- `requirements.txt`: shared dependencies

If any of the files listed above are missing, follow the variant-specific README to recreate or reconfigure as needed.

## Prerequisites
- Python 3.12 or newer
- Windows PowerShell or a compatible shell
- An active virtual environment
- Internet access for model API calls

## Environment Variables
Create a `.env` file in the repository root (same folder as `requirements.txt`). At minimum, you will need credentials for Google Generative AI via Google ADK.

Common variables:
- `GOOGLE_API_KEY=<your_api_key>`
- Any other keys required by your environment

Ensure `python-dotenv` is installed (it is listed in `requirements.txt`).

## Setup
1) Create and activate a virtual environment (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2) Install dependencies:
```powershell
pip install -r requirements.txt
```

3) Confirm package layout:
- `Project/customer_service_agent` exists and contains `__init__.py`, `agent.py`, `utils.py`, and the `tools` directory

## How to Run

### CLI Variant
Refer to `Project/README_CLI.md` for full details. Typical command:
```powershell
cd Project\customer_service_agent
python main.py
```

### Streamlit Variant
Refer to `Project/README_Streamlit.md` for full details. Typical command:
```powershell
streamlit run Project/Customer_service_agent/app.py
```
If the Streamlit entry point is not present, follow the Streamlit README to create or restore it.

## Troubleshooting
- Module import errors for `customer_service_agent`:
  - Launch from the repository root so relative imports resolve
  - Ensure `__init__.py` is present in `Project/customer_service_agent`
  - Optionally set `PYTHONPATH` to include the `Project` directory
- Asynchronous call errors (e.g., coroutine not awaited):
  - Ensure async methods on the session service and runner are awaited
- Authentication or model API errors:
  - Confirm `.env` contains valid API keys and required configuration
  - Restart the shell after adding environment variables

## Extending the Project
- Add new sub-agents under `Project/customer_service_agent/tools/` and register them in `agent.py`
- Extend `utils.py` to track additional session state keys
- Keep UI-specific code out of the core package to preserve reuse across variants

## Additional Documentation
- CLI variant: `Project/README_CLI.md`
- Streamlit variant: `Project/README_Streamlit.md`



