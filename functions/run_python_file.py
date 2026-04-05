import os
from pathlib import Path
import sys
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_path])!=working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not Path(target_path).suffix == ".py":
            return f'Error: "{file_path}" is not a Python file' 
        command = ["python", target_path]
        if args:
            command.extend(args)
        result_process = subprocess.run(command, cwd = working_dir_abs, capture_output=True, text=True, timeout= 30)
        returned_string = ""
        if result_process.returncode != 0:
            returned_string += f'Process exited with code {result_process.returncode}'
        if result_process.stderr == "" and result_process.stdout == "":
            returned_string += "No output produced"
        if result_process.stderr != "": 
            returned_string += f"STDERR:\n{result_process.stderr}"
        if result_process.stdout != "":
            returned_string += f"STDOUT:\n{result_process.stdout}"
            
        return returned_string
    except Exception as e:
         return f"Error: {e}" 

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="takes a path, and maybe some args, to try and execute a .py located inside the working directory and return a string with the result of the executions",
    parameters=types.Schema(
        type = types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type = types.Type.STRING,
                description="path to the .py to execute"
            ),
            "args": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(type=types.Type.STRING),
                    description="complementary arguments eventually needed to execute the .py"
            )
        },
        required=["file_path"]
    )
)