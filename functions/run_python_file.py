import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path): 
    file_path_abs = ""
    working_directory_abs = ""
    # is working directory real?
    try:
        working_directory_abs = os.path.abspath(working_directory)
    except:
        return f"Error: {working_directory} not found."
    
    if os.path.isdir(working_directory_abs) == False:
        return f'Error: "{working_directory}" is not a directory'
    
    # Is our target directory legal/within the working directory
    try:
        file_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))
    except:
        return f'Error: File "{file_path}" not found.'
    
    try:
        if os.path.exists(file_path_abs) == False:
           return f'Error: File "{file_path}" not found.'
    except:
        return f'Error: File "{file_path}" not found.'
    
    if file_path_abs.startswith(working_directory_abs) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.splitext(file_path)[1] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    ret = ""
    try:
        complete = subprocess.run(["python3", file_path_abs],capture_output=True,timeout=30)
        complete_split = str(complete).split(",")
        for part in complete_split:
            if "stdout" in part and part.split("=")[1] !="b''":
                ret += f"STDOUT: {part.split("=")[1]}\n"
            if "stderr" in part and part.split("=")[1] !="b=''":
                ret += f"STDERR: {part.split("=")[1]}\n"
            if "returncode" in part and part.split("=")[1] != "0":
                ret += f"Process exited with code {part.split("=")[1]}"
        
        if len(ret) == 0:
            return "No output produced"
        return ret
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Using the specified file path, executes a python script. Constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file to execute",
            )
        },
    ),
)