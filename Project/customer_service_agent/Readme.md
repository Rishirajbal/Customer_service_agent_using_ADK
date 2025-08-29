# Customer Service Agent (CLI Only)

This guide explains how to install, configure, and run the Customer Service Agent from the command line without any Streamlit UI. It assumes the Python package with the agents lives under `Project/customer_service_agent`.

## Contents
- Overview
- Prerequisites
- Environment variables
- Setup (Windows PowerShell)
- Running the CLI
- Project structure reference
- Troubleshooting
- Extending

## Overview
The CLI application runs an interactive terminal chat loop, backed by the same agent and sub-agents used in the UI version. Session state is stored in memory for the lifetime of the process.

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

2) Install dependencies:
```powershell
pip install -r requirements.txt
```

3) Verify the package directory exists:
- `Project/customer_service_agent/` must contain `__init__.py`, `agent.py`, `utils.py`, and the `tools` directory.

## Running the CLI
From the repository root (folder containing `requirements.txt`):
```powershell
cd Project\customer_service_agent
python main.py
```
Behavior:
- Enter a message and press Enter to send it to the agent.
- Type `exit` or `quit` to end the session.
- The application prints the final in-memory session state before exiting.

## Project structure reference
- `Project/customer_service_agent/agent.py`: defines the primary agent and sub-agents.
- `Project/customer_service_agent/tools/`: specialized agents used by the main agent.
- `Project/customer_service_agent/utils.py`: utility functions for session state and agent execution.
- `Project/customer_service_agent/main.py`: CLI entry point (async loop) that wires runner, session service, and message handling.

## Troubleshooting
- ModuleNotFoundError: `customer_service_agent`
  - Run the CLI from inside `Project/customer_service_agent` as shown.
  - Ensure `__init__.py` exists in the package folder.
  - If running from elsewhere, set the Python path to include the parent directory. Example:
    ```powershell
    setx PYTHONPATH "%CD%\Project"
    # Open a new shell after setting, or temporarily use:
    $env:PYTHONPATH = (Resolve-Path .\Project).Path
    ```

- "coroutine was never awaited" or similar async errors
  - Ensure your `main.py` awaits all async operations on the session service and runner.

- Authentication / API issues
  - Confirm your `.env` contains a valid `GOOGLE_API_KEY` and any other required variables.
  - Restart the shell or reload environment if variables were added after activation.

## Extending
- Add new tools/agents under `Project/customer_service_agent/tools/` and include them in `agent.py`.
- Add new state fields in `utils.py` and update any display or persistence logic as needed.
