import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_wd = os.path.abspath(working_directory)
        abs_fp = os.path.normpath(os.path.join(abs_wd, file_path))
        valid_fp = os.path.commonpath([abs_wd, abs_fp]) == abs_wd
    except Exception as e:
        raise Exception(f'Error processing file path "{file_path}": {e}')
    
    if not valid_fp:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory.'
    
    if not os.path.isfile(abs_fp):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_fp, 'r') as f:
            content = f.read(MAX_CHARS)  # Read up to MAX_CHARS characters
            if f.read(1):  # Check if there's more content beyond the limit
                content += f'[...File "{file_path}" truncated after {MAX_CHARS} characters]'
        return content
    except Exception as e:
        raise Exception(f'Error reading file "{file_path}": {e}')
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file relative to the working directory, up to a maximum number of characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)