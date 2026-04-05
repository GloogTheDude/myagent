from google.genai import types
import functions.get_files_info as gfi 
import functions.get_file_content as gfc
import functions.run_python_file as rpf
import functions.write_file as wf


available_functions = types.Tool(
    function_declarations=[gfi.schema_get_files_info,
                           gfc.schema_get_file_content,
                           rpf.schema_run_python_file,
                           wf.schema_write_file]
                           
)

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    function_map = {
    "get_file_content": gfc.get_file_content,
    "get_files_info": gfi.get_files_info,
    "run_python_file": rpf.run_python_file,
    "write_file": wf.write_file
    }

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    else:
        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = "./calculator"
        function_result = function_map[function_name](**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )