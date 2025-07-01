from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Lists files in the specified directory along with their sizes, "
        "constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory to list files from, relative to the working directory. "
                    "If not provided, lists files in the working directory itself."
                ),
            ),
        },
    ),
)
import os


from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = os.path.abspath(os.path.join(working_directory,directory))
    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_target_path):
        return f'Error: "{directory}" is not a directory'
    try:
        files = os.listdir(abs_target_path)
        list_of_strings_of_files = []
        for file in files:
            file_path = os.path.join(abs_target_path,file)
            file_size = os.path.getsize(file_path)
            is_file_dir = os.path.isdir(file_path)
            temp_string = f"- {file}: file_size={file_size}, is_dir={is_file_dir}"
            list_of_strings_of_files.append(temp_string)
        output = "\n".join(list_of_strings_of_files)
        return output
    except Exception as e:
        return f"Error: {e}"
        
    