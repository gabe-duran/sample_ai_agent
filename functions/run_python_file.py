import os
import subprocess
from google.genai import types

def run_python_file(working_directory: str, file_path: str, args=[]):
    base = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(base, file_path))

    if os.path.commonpath([base, target]) != base:
       return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target):
        return f'Error: File "{file_path}" not found.'

    if not target.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(["python", target, *args], timeout=30, capture_output=True, cwd=base )

        stdout = completed_process.stdout
        stderr = completed_process.stderr
        exit_code = completed_process.returncode

        message = []

        if not stdout and not stderr:
            return "No output produced."
        if stdout:
            message.append(f"STDOUT: {stdout}")
        if stderr:
            message.append(f"STDERR: {stderr}")
        if exit_code != 0 :
            message.append(f"Process exited with code {exit_code}")

        return "\n".join(message)

    except Exception as e:
        return f"Error: executing Python file: {str(e)}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Runs the specified Python file within the working directory."
        "Accepts command-line arguments as a list of strings."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description=(
                    "Optional list of command-line arguments to pass to the script. "
                    "If omitted, the script runs with no arguments."
                ),
                items=types.Schema(type=types.Type.STRING)
            ),
        },
        required=["file_path"],
    ),
)