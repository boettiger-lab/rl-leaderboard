
from datetime import datetime
import csv
import os
import hashlib
 
def filehash(filename):
  with open(filename,"rb") as f:
    bytes = f.read() # read entire file as bytes
    readable_hash = hashlib.sha256(bytes).hexdigest();
    return readable_hash

def leaderboard(agent, env, team, mean, std, hashid, file = "leaderboard.csv"):
    
    ## FIXME only add score if hashid (or hashid+env) is not already found? 
    row_contents = {"agent": agent,
                    "env": env,
                    "team": team,
                    "mean": mean, 
                    "std": std,
                    "id": hashid,
                    "date": datetime.now()}
    has_header = os.path.exists(file)                
    with open(file, 'a+') as stream:
        writer = csv.DictWriter(stream, 
                                fieldnames = ["agent", 
                                              "env",
                                              "team",
                                              "mean", 
                                              "std", 
                                              "id", 
                                              "date"])
        if(not has_header):                                      
            writer.writeheader()
        writer.writerow(row_contents)


# leaderboard("X", "B", 3, 0, "leaderboard.py", "test.csv")
