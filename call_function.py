from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args.copy()
    args["working_directory"] = WORKING_DIR
    call_to_make = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_call_part.name not in call_to_make:
        return types.Content(
        role="tool",
        parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
        ],
    )
    
    res = call_to_make[function_call_part.name](**args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": res},
        )
    ],
)
