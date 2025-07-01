from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file and returns its output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory.",
            ),
        },
    ),
)
import os
import subprocess


def run_python_file(working_directory, file_path):
    """
    Runs a Python file using 'uv run' in the specified working directory.
    Captures and returns stdout and stderr, with appropriate prefixes and error handling.
    """
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: File "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["uv", "run", abs_file_path],
            timeout=30,
            cwd=abs_working_dir,
            capture_output=True,
            text=True
        )
        output = ""
        if result.stdout:
            output += f"STDOUT: {result.stdout}"
        if result.stderr:
            output += f"STDERR: {result.stderr}"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not output.strip():
            output = "No output produced."
        return output
    except Exception as e:
        return f"Error during execution: {str(e)}"