import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_wd = os.path.abspath(working_directory)
        abs_fp = os.path.normpath(os.path.join(abs_wd, file_path))
        valid_fp = os.path.commonpath([abs_wd, abs_fp]) == abs_wd
    except Exception as e:
        raise Exception(f'Error processing file path "{file_path}": {e}')
    
    if not valid_fp:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    
    if not os.path.isfile(abs_fp):
        return f'Error: "{file_path}" does not exist or is not a regular file'
        
    if not abs_fp.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        command = ["python", abs_fp]

        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}. Stderr: {result.stderr}"
        if len(result.stdout) == 0 and len(result.stderr) == 0:
            return "No output produced"
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        raise Exception(f'Error: executing Python file "{file_path}": {e}')
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file relative to the working directory, optionally with arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)