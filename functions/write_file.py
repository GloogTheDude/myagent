import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    try:
        if os.path.commonpath([working_dir_abs, target_path])!=working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent = os.path.dirname(target_path) 
        os.makedirs(parent, exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write some given content into a given file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to file file in which the content sould be writen",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description="the content who's exepected to be written in the file"
            )
        },
        required=["file_path", "content"]
    ),
)
