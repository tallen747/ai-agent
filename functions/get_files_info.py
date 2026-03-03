import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_wd = os.path.abspath(working_directory)
        abs_td = os.path.normpath(os.path.join(abs_wd, directory))
        valid_td = os.path.commonpath([abs_wd, abs_td]) == abs_wd
    except Exception as e:
        raise Exception(f'Error processing directory "{directory}": {e}')
    
    if not valid_td:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory.'
        #raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory.')
    
    if not os.path.isdir(abs_td):
        return f'Error: "{directory}" is not a directory.'
        #raise Exception(f'Error: "{directory}" is not a directory.')
    
    try:
        files = os.listdir(abs_td)
        files_info = []

        for file in files:
            file_path = os.path.join(abs_td, file)
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            files_info.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")

        return files_info
    except Exception as e:
        raise Exception(f'Error listing files in "{directory}": {e}')
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)