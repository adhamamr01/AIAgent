

def call_function(function_call_part, verbose=False):
    """
    Handles calling one of the four available functions based on the function_call_part.
    Returns a types.Content with the function result or error.
    """
    name = function_call_part.name
    args = dict(function_call_part.args or {})

    # Import the actual function implementations
    from functions.get_files_info import get_files_info
    from functions.get_file_content import get_file_content
    from functions.run_python import run_python_file
    from functions.write_file import write_file
    from google.genai import types

    # Map function names to implementations
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    # Always set working_directory to ./calculator
    args["working_directory"] = os.path.abspath("./calculator")

    if verbose:
        print(f"Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    func = function_map.get(name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    try:
        # Remove working_directory from args for passing as kwarg
        result = func(**args)
    except Exception as e:
        result = f"Error during function call: {e}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_files_info import available_functions


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Answer questions based on the files in the working directory
- Search files for fixing bugs while explaining in steps what was done or finding information

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) == 1:
    print("You need to supply a message.")
    sys.exit(1)


user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

def print_function_result(function_call_result, verbose):
    # Check for valid function response
    try:
        response_obj = function_call_result.parts[0].function_response.response
    except Exception:
        raise RuntimeError("Fatal: No function response in Content returned by call_function.")
    if verbose:
        print(f"-> {response_obj}")

max_iterations = 20
iteration = 0
while iteration < max_iterations:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # Add all candidate contents to the conversation
    candidates = getattr(response, "candidates", None)
    if candidates:
        for candidate in candidates:
            if hasattr(candidate, "content") and candidate.content:
                messages.append(candidate.content)

    # Handle function calls using call_function
    function_calls = getattr(response, "function_calls", None)
    function_call = getattr(response, "function_call", None)
    function_called = False

    if function_calls:
        for function_call_part in function_calls:
            function_call_result = call_function(function_call_part, verbose=(len(sys.argv) == 3 and sys.argv[2] == "--verbose"))
            print_function_result(function_call_result, verbose=(len(sys.argv) == 3 and sys.argv[2] == "--verbose"))
            messages.append(function_call_result)
            function_called = True
    elif function_call is not None:
        function_call_result = call_function(function_call, verbose=(len(sys.argv) == 3 and sys.argv[2] == "--verbose"))
        print_function_result(function_call_result, verbose=(len(sys.argv) == 3 and sys.argv[2] == "--verbose"))
        messages.append(function_call_result)
        function_called = True
    else:
        # No function call, print final response and break
        print(response.text)
        break

    iteration += 1

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
),
)



# Handle function calls using call_function
function_calls = getattr(response, "function_calls", None)
function_call = getattr(response, "function_call", None)

def print_function_result(function_call_result, verbose):
    # Check for valid function response
    try:
        response_obj = function_call_result.parts[0].function_response.response
    except Exception:
        raise RuntimeError("Fatal: No function response in Content returned by call_function.")
    if verbose:
        print(f"-> {response_obj}")

if function_calls:
    for function_call_part in function_calls:
        function_call_result = call_function(function_call_part, verbose=(len(sys.argv) == 3 and sys.argv[2] == "--verbose"))
        print_function_result(function_call_result, verbose=(len(sys.argv) == 3 and sys.argv[2] == "--verbose"))
elif function_call is not None:
    function_call_result = call_function(function_call, verbose=(len(sys.argv) == 3 and sys.argv[2] == "--verbose"))
    print_function_result(function_call_result, verbose=(len(sys.argv) == 3 and sys.argv[2] == "--verbose"))
else:
    print(response.text)

if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")