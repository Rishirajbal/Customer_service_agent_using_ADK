# Customer Service Agent (Streamlit UI)

This guide explains how to install, configure, and run the Customer Service Agent with a Streamlit user interface. It assumes the Python package with the agents lives under `Project/customer_service_agent`, and the Streamlit entry point is `Project/Customer_service_agent/app.py` (or an equivalent path you choose).

## Contents
- Overview
- Prerequisites
- Environment variables
- Setup (Windows PowerShell)
- Running the Streamlit app
- Project structure reference
- Import path notes
- Troubleshooting
- Extending

## Overview
The Streamlit app provides a simple chat interface on top of the same agent logic used by the CLI version. Session state is kept in memory per Streamlit session.

## Prerequisites
- Python 3.12 or newer
- A virtual environment (recommended)
- Internet access to call model APIs

## Environment variables
Create a `.env` file at the repository root (same folder as `requirements.txt`). At minimum you will need credentials for Google Generative AI via Google ADK/generativeai libraries.

Common variables:
- GOOGLE_API_KEY=<your_api_key>
- (Any additional keys your environment requires)

Ensure `.env` is readable and that `python-dotenv` is listed in `requirements.txt`.

## Setup (Windows PowerShell)
1) Create and activate a virtual environment:
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2) Install dependencies (includes Streamlit):
```powershell
pip install -r requirements.txt
```

3) Verify directories:
- `Project/customer_service_agent/` contains the reusable agent package (with `__init__.py`).
- `Project/Customer_service_agent/app.py` exists as the Streamlit entry point (or adjust paths below to your chosen location).

## Running the Streamlit app
From the repository root (folder containing `requirements.txt`):
```powershell
streamlit run Project/Customer_service_agent/app.py
```
By default, Streamlit will open your browser to the app. Use the chat input to send messages to the agent.

## Project structure reference
- `Project/customer_service_agent/agent.py`: defines the main agent and sub-agents.
- `Project/customer_service_agent/tools/`: specialized agents used by the main agent.
- `Project/customer_service_agent/utils.py`: shared utility functions the UI may import.
- `Project/Customer_service_agent/app.py`: Streamlit entry point that imports the agent and session services and renders the chat UI.

## Import path notes
- If the app cannot import `customer_service_agent`, ensure Streamlit is launched from the repository root so that the relative path setup in the app can locate the sibling package.
- Alternatively, set `PYTHONPATH` to include the `Project` directory. Example:
  ```powershell
  setx PYTHONPATH "%CD%\Project"
  # Open a new shell after setting, or temporarily use:
  $env:PYTHONPATH = (Resolve-Path .\Project).Path
  ```
- As a last resort, you can prepend the parent folder to `sys.path` at the top of `app.py`:
  ```python
  import os, sys
  BASE_DIR = os.path.dirname(os.path.dirname(__file__))
  if BASE_DIR not in sys.path:
      sys.path.append(BASE_DIR)
  ```

## Troubleshooting
- ModuleNotFoundError: `customer_service_agent`
  - Launch Streamlit from the repository root and verify `__init__.py` exists inside `Project/customer_service_agent`.
  - Use the `PYTHONPATH` guidance above if launching from a different working directory.

- Pydantic or agent parent assignment errors
  - Ensure the agent graph is initialized exactly once. Avoid re-importing or manually instantiating the same sub-agent tree multiple times in the same process.

- Authentication / API issues
  - Confirm your `.env` contains a valid `GOOGLE_API_KEY` and any other required variables.
  - Restart the shell or reload environment if variables were added after activation.

## Extending
- Add new tools/agents under `Project/customer_service_agent/tools/` and include them in `agent.py`.
- Add UI elements to `app.py` for richer interactions, but keep the agent logic inside the reusable package under `Project/customer_service_agent`.
