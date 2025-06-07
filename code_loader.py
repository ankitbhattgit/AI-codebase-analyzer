import os
from typing import List, Dict

# Recursively loads all files in the given directory and returns list of dictionaries with keys
def load_files(root_dir: str) -> List[Dict[str, str]]:

    project_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".java"):
                full_path = os.path.join(dirpath, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        project_files.append({
                            "path": full_path,
                            "content": content
                        })
                except Exception as e:
                    print(f"Error reading file {full_path}: {e}")

    return project_files