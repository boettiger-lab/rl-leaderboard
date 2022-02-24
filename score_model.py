#!/usr/local/python

from stable_baselines3 import A2C, PPO, SAC, DDPG, TD3, DQN, HER

import gym
import yaml
import glob
import os
import re
import argparse

# sb3_contrib algorithms are imported conditionally only
try:
    from sb3_contrib import ARS, TRPO, MaskablePPO, QRDQN, TQC
    CONTRIB = {
         "ARS": ARS,
         "TRPO": TRPO,
         "TQC": TQC,
         "MaskablePPO": MaskablePPO,
         "QRDQN": QRDQN}
except ImportError:
    CONTRIB = {}

from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

from github_hash_url import github_hash_url
from leaderboard import leaderboard, filehash
import pandas as pd
# seed = 12345

MODEL = {"PPO": PPO,
         "A2C": A2C,
         "SAC": SAC,
         "DDPG": DDPG,
         "TD3": TD3,
         "DQN": DQN,
         "HER": HER
        }
# extend with contrib
MODEL.update(CONTRIB)

def import_gym(env_name):
    if "fishing" in env_name:
        import gym_fishing
    elif "ays" in env_name or "dice" in env_name:
        import gym_climate
    elif "wildfire" in env_name:
        import gym_wildfire
    elif "conservation" in env_name:
        import gym_conservation
    elif "sir" in env_name:
        import gym_epidemic

def score_model(env_name, agent_name, model_name, team, hash_url, hash_file, file):
    import_gym(env_name)
    env = Monitor(gym.make(env_name))
    agent = MODEL[agent_name]
    model = agent.load(model_name[:-4])
    score = evaluate_policy(model, env, n_eval_episodes=100)
    print(team + ", " + env_name + ", " + agent_name + ": ", score[0])
    leaderboard(agent = agent_name, 
                env = env_name,
                team = team, 
                mean = score[0], 
                std = score[1],
                hash_url = hash_url,
                hash_file = hash_file,
                file = "../leaderboard.csv")


# NOTE: ideally should take a path to leaderboard.csv
def main():  # noqa: C901
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directory name with model", type=str)
    args = parser.parse_args()
    model_names = glob.glob(f"{args.dir}/*.zip")
    leaderboard_csv = "../leaderboard.csv"

    for model_name in model_names:
        parsed = re.search("([a-zA-Z]+\-v\d+)\-([A-Z0-9]+)\-(\w+)\.zip", model_name)
        env_name = parsed.group(1)
        agent_name = parsed.group(2)
        team = parsed.group(3)
        hash_url = github_hash_url(model_name, f"{args.dir}")
        hash_file = filehash(model_name)
        if os.path.exists(leaderboard_csv):
            leaderboard = pd.read_csv(leaderboard_csv)
            if hash_file not in leaderboard['hash_file'].values:
                try:
                    score_model(env_name, agent_name, model_name, team, hash_url, hash_file, file=leaderboard_csv)
                except Exception as error:
                    with open("nonscored_submissions.txt", "w") as f:
                        f.write(f"{model_name} : {error}")
        else:
            try:
                score_model(env_name, agent_name, model_name, team, hash_url, hash_file, file=leaderboard_csv)
            except Exception as error: 
                with open("nonscored_submissions.txt", "w") as f:
                    f.write(f"{model_name} : {error}")


if __name__ == "__main__":
    main()
