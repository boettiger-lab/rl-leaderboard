## Note: If a script is edited after it starts running but before the leaderboard
## calculation is performed, it will commit the modified version and not the 
## one that matches the execution.  
## So best to call hash_url early in execution and pass to leaderboard.

from git import Repo
import os

def github_hash_url(script):
    ## Commit file and compute GitHub URL
    repo = Repo(".", search_parent_directories=True)
    path = os.path.relpath(script, repo.git.working_dir)
    repo.git.add(path)
    if len(repo.index.diff("HEAD")) > 0:
        repo.git.commit("-m 'robot commit before running script'")
    sha = repo.commit().hexsha
    url = repo.git.remote("get-url", "origin")[:-4] + "/blob/" + sha + "/" + path
    return url

