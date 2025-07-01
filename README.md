# AI Coding Agent

## Overview
This project is an AI-powered coding agent that can:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Answer questions based on the files in the working directory
- Search files for fixing bugs or finding information, while explaining the steps taken

The agent uses Google Gemini's LLM API to plan and execute tasks, calling Python functions as needed and maintaining a conversation history for multi-step reasoning.

## How It Works
1. The user provides a prompt (question or request) to the agent.
2. The agent plans a sequence of function calls to accomplish the task, using the available tools.
3. Each function call is executed in a secure, sandboxed way, with results fed back into the conversation.
4. The agent iterates up to 20 times, updating its plan based on new information, until the task is complete or a final answer is produced.

## Usage
Run the agent from the command line:

```bash
uv run main.py "<your prompt>" [--verbose]
```

Example prompts:
- `what files are in the root?`
- `show me the contents of calculator/pkg/calculator.py`
- `run calculator/pkg/calculator.py`
- `write a file called test.txt with the text hello world`

Use `--verbose` to see detailed function call and result output.

## Project Structure
- `main.py` — Main entry point and agent loop
- `functions/` — Contains all callable function implementations and their schemas
- `calculator/` — Example working directory for file operations

## Security
All file operations are restricted to the `./calculator` directory for safety. The agent will not access files outside this directory.

## Requirements
- Python 3.8+
- `uv` (for running Python files)
- Google Gemini API key (set as `GEMINI_API_KEY` in a `.env` file)

## Setup
1. Install dependencies:
   - `pip install -r requirements.txt`
2. Set up your `.env` file with your Gemini API key:
   - `GEMINI_API_KEY=your_api_key_here`
3. Run the agent as shown above.
