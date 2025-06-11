import os
def get_file_content(working_directory, file_path):
    print("in")
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
        file_path_abs = os.path.join(working_directory_abs, file_path)
    except:
        return f"Error: {file_path} not found."
    
    print(file_path_abs)
    if file_path_abs.startswith(working_directory_abs) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(file_path_abs) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    with open(file_path_abs, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == MAX_CHARS:
            file_content_string += f'[...File "{file_path_abs}" truncated at 10000 characters]'
        return file_content_string
    