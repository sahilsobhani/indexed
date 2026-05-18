import ast
from pathlib import Path

def build_chunk(chunk_type, name, file_path, content):
    """Build a metadata chunk for indexing."""
    return {
        "type": chunk_type,
        "name": name,
        "file_name": Path(file_path).name,
        "file_path": str(file_path),
        "content": content
    }

def chunk_python_file(file_path):
    """Create chunks for functions and module-level assignments in a Python file."""
    with open(file_path, "r", encoding ="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)

    chunks = []

    for node in tree.body:
        # Capture each top-level function as its own chunk.
        if isinstance(node, ast.FunctionDef):
            chunk = build_chunk("function", node.name, file_path, ast.get_source_segment(code, node))

            chunks.append(chunk)

        # Capture plain assignments like FOO = 1 or index = faiss.IndexFlatL2(...).
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                # Only index simple variable names, not attributes or tuple unpacking.
                if isinstance(target, ast.Name):
                    chunk_type = "constant" if target.id.isupper() else "global"
                    chunk = build_chunk(chunk_type, target.id, file_path, ast.get_source_segment(code, node))

                    chunks.append(chunk)

        # Capture annotated assignments like TIMEOUT: int = 30.
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name):
                chunk_type = "constant" if node.target.id.isupper() else "global"
                chunk = build_chunk(chunk_type, node.target.id, file_path, ast.get_source_segment(code, node))

                chunks.append(chunk)

    return chunks
