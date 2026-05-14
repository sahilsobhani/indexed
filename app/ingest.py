from git import Repo
from pathlib import Path

def clone_repo(repo_url: str):
    repo_name = repo_url.split("/")[-1].replace(".git", "")

    local_path = Path("repos") / repo_name

    if local_path.exists():
        return str(local_path)
    
    Repo.clone_from(repo_url, local_path)

    return str(local_path)