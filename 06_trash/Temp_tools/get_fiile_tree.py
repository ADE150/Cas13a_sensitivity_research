from common_tools import *

def generate_directory_structure(root_dir, ignore_list):
    directory_structure = []

    def walk_directory(current_dir, level):
        indent = ' ' * 4 * level
        base_dir = os.path.basename(current_dir)
        directory_structure.append(f"{indent}- {base_dir}/")

        if base_dir in ignore_list:
            return  # Skip subdirectories and files of ignored directories

        subindent = ' ' * 4 * (level + 1)
        try:
            entries = os.listdir(current_dir)
            entries.sort()  # Sort entries for consistent output
            for entry in entries:
                path = os.path.join(current_dir, entry)
                if os.path.isdir(path):
                    walk_directory(path, level + 1)
                else:
                    directory_structure.append(f"{subindent}- {entry}")
        except PermissionError:
            pass  # Skip directories for which the user does not have permission

    walk_directory(root_dir, 0)
    return '\n'.join(directory_structure)

ignore_list = [".git", "__pycache__", ".idea"]
# root_dir = os.getcwd()
directory_structure_markdown = generate_directory_structure(root_dir, ignore_list)
print(directory_structure_markdown)
