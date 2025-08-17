import os
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    base = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(base, file_path))

    #print(f"base: {base}")
    #print(f"target: {target}")

    if os.path.commonpath([base, target]) != base:
       return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target):
       return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)

        truncated_file_message = ''
        if len(file_content_string) > MAX_CHARS:
            truncated_file_message = f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {str(e)}"

    return file_content_string[:MAX_CHARS] + truncated_file_message

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves the contents of the specified file up to {MAX_CHARS}.  If the file is longer than {MAX_CHARS} the file will be truncated and a message appended. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)