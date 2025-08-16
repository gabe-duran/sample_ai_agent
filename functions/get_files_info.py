import os

def get_files_info(working_directory, directory="."):
    relative = os.path.join(working_directory, directory)
    target = os.path.abspath(relative)
    base = os.path.abspath(working_directory)

    if os.path.commonpath([base, target]) != base:
       return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'

    lines = []
    for item in os.listdir(target):
        item_path = os.path.join(target, item)
        try:
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path)
        except Exception as e:
            return f"Error: {str(e)}"
        lines.append(f"- {item}: file_size={size}, is_dir={is_dir}")

    return "\n".join(lines)

def main():
    print(get_files_info("calculator","."))


if __name__ == "__main__":
    main()