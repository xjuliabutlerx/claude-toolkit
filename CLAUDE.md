# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python 3.11+ CLI toolkit. Each tool is a standalone script in the `tools/` directory.

## Adding a New Tool

1. Create the script in `tools/<tool_name>.py`
2. Every tool must include:
   - A module-level docstring describing what it does
   - A usage example in the docstring (e.g., `python tools/<tool_name>.py --arg value`)
   - A `if __name__ == "__main__":` entry point
3. After creating the tool, update `README.md` with the tool name and a one-line description of what it does

## Running Tools

```bash
python tools/<tool_name>.py
python tools/<tool_name>.py --help
```

## Requirements

- Python 3.11+
- Some tools require third-party packages. Set up the virtual environment once:
  ```bash
  python -m venv .venv
  source .venv/bin/activate   # macOS/Linux
  pip install Pillow pillow-heif
  ```
- Activate the venv before running tools that use third-party libraries:
  ```bash
  source .venv/bin/activate
  ```
