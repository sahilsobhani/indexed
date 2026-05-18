import ast
from pathlib import Path

def chunk_python_file(file_path):
    with open(file_path, "r", encoding ="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)

    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            chunk = {
                "type":"function",
                "name": node.name,
                "file_name": Path(file_path).name,
                "file_path": str(file_path),
                "content": ast.get_source_segment(code, node)
            }

            chunks.append(chunk)

    return chunks
