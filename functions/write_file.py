import os
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str):
    base = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(base, file_path))

    if os.path.commonpath([base, target]) != base:
       return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target):
        try:
            os.makedirs(os.path.dirname(target), exist_ok=True)
        except Exception as e:
            return f"Error creating directory: {str(e)}"

    if os.path.isdir(target):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(target, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: writing to file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes the specified content to a file within the working directory. "
        "Overwrites the file if it exists. Creates parent directories as needed."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file."
            ),
        },
    ),
)