import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    # print("get_files_info_start")
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    # print(f"gonna try {target_dir}")
    try:
        if(valid_target_dir):
            if os.path.isdir(target_dir):
                return list_item_directory(target_dir)
            else:return f'Error: "{directory}" is not a directory'
        else: return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"

def list_item_directory(working_path):
    dir_item = os.listdir(working_path)
    formated_strings = []
    for i in dir_item:
        file_name = i
        file_size = os.path.getsize(os.path.join(working_path,i))
        is_dir = os.path.isdir(os.path.join(working_path,i))
        formated_string = f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir} "
        formated_strings.append(formated_string)
    return "\n".join(formated_strings)

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