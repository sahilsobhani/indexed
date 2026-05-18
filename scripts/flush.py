import os
import stat
import shutil
from pathlib import Path


STORAGE_FILES = [
    Path("storage/code.index"),
    Path("storage/metadata.json"),
    Path("storage/conversation.json"),
]

REPOS_DIR = Path("repos")


def delete_file(path):
    """Delete a file if it exists."""
    if path.exists():
        path.unlink()
        print(f"Deleted file: {path}")


def delete_repo_directories():
    """Delete all cloned repositories."""
    if not REPOS_DIR.exists():
        return

    for repo_dir in REPOS_DIR.iterdir():
        if repo_dir.is_dir():
            shutil.rmtree(repo_dir, onerror=handle_remove_readonly)
            print(f"Deleted repo: {repo_dir}")


def handle_remove_readonly(func, path, exc_info):
    """Retry deleting a read-only path on Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def flush():
    """Clear generated indexes, metadata, conversation history, and cloned repos."""
    for storage_file in STORAGE_FILES:
        delete_file(storage_file)

    delete_repo_directories()
    print("Flush complete.")


if __name__ == "__main__":
    flush()
