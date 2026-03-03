import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        abs_wd = os.path.abspath(working_directory)
        abs_fp = os.path.normpath(os.path.join(abs_wd, file_path))
        valid_fp = os.path.commonpath([abs_wd, abs_fp]) == abs_wd
    except Exception as e:
        raise Exception(f'Error processing file path "{file_path}": {e}')
    
    if not valid_fp:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory.'
    
    if os.path.isdir(abs_fp):
        return f'Error: Cannot write to "{file_path}" as it is a directory.'
    
    os.makedirs(os.path.dirname(abs_fp), exist_ok=True)  # Create directories if they don't exist
    
    try:
        with open(abs_fp, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        raise Exception(f'Error writing to file "{file_path}": {e}')
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the specified file",
            ),
        },
    ),
)