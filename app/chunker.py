import ast

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
                "content": ast.get_source_segment(code, node)
            }

            chunks.append(chunk)

    return chunks
