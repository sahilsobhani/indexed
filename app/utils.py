from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".go"
}

IGNORE_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "__pycache__"
}

def get_code_files(repo_path):
    """Collect supported source files while skipping ignored directories."""

    files = []

    for file in Path(repo_path).rglob("*"):
        if any(part in IGNORE_DIRS for part in file.parts):
            continue

        if file.suffix in SUPPORTED_EXTENSIONS:
            files.append(file)

    return files
