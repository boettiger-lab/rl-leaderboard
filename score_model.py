#!/usr/local/python

from stable_baselines3 import A2C, PPO, SAC, DDPG, TD3, DQN
import gym
import yaml
import glob
import os
import re
import argparse

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
         "DQN": DQN}

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

def score_model(env_name, agent_name, model_name, team, hash_url, hash_file):
    import_gym(env_name)
    env = Monitor(gym.make(env_name))
    agent = MODEL[agent_name]
    model = agent.load(model_name[:-4])
    score = evaluate_policy(model, env, n_eval_episodes=100)
    leaderboard(agent = agent_name, 
                env = env_name,
                team = team, 
                mean = score[0], 
                std = score[1],
                hash_url = hash_url,
                hash_file = hash_file,
                file = "leaderboard.csv")


def main():  # noqa: C901
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directory name with model", type=str)
    args = parser.parse_args()
    model_name = glob.glob(f"models/{args.dir}/*.zip")[0]
    
    
    parsed = re.search("([a-zA-Z]+\-v\d+)\-([A-Z0-9]+)\-(\w+)\.zip", model_name)
    env_name = parsed.group(1)
    agent_name = parsed.group(2)
    team = parsed.group(3)
    hash_url = github_hash_url(model_name)
    hash_file = filehash(model_name)
    if os.path.exists("leaderboard.csv"):
        leaderboard = pd.read_csv("leaderboard.csv")
        if hash_file not in leaderboard['hash_file'].values:
            score_model(env_name, agent_name, model_name, team, hash_url, hash_file)
    else:
        score_model(env_name, agent_name, model_name, team, hash_url, hash_file)


if __name__ == "__main__":
    main()
