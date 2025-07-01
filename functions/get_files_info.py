import os
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
        