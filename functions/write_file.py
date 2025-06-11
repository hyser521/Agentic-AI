import os
def write_file(working_directory, file_path, content):
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
        return f"Error: {file_path} not found."
    
    if file_path_abs.startswith(working_directory_abs) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if os.path.exists(file_path) == False:
        os.makedirs(os.path.basename(file_path_abs), exist_ok=True)

    

    with open(file_path_abs, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    
    