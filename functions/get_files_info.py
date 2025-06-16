import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory == None:
        directory = ""
    working_directory_abs = ""
    directory_abs = ""

    # is working directory real?
    try:
        working_directory_abs = os.path.abspath(working_directory)
    except:
        return f"Error: {working_directory} not found."
    
    if os.path.isdir(working_directory_abs) == False:
        return f'Error: "{working_directory}" is not a directory'
    
    # Is our target directory legal/within the working directory
    try:
        directory_abs = os.path.abspath(os.path.join(working_directory_abs, directory))
    except:
        return f"Error: {directory} not found."

    if os.path.isdir(directory_abs) == False or directory_abs.startswith(working_directory_abs) == False:
        return f'Error: Cannot read "{directory}" as it is outside the permitted working directory'
    
    directory_contents = list(map(lambda x: f"- {x}: file_size={os.path.getsize(os.path.join(directory_abs, x))}, is_dir={os.path.isdir(os.path.join(directory_abs, x))}", os.listdir(directory_abs)))
    ret = "\n".join(directory_contents)
    return ret

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

    