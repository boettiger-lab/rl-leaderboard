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

from leaderboard import leaderboard, filehash
# seed = 12345

MODEL = {"PPO": PPO,
         "A2C": A2C,
         "SAC": SAC,
         "DDPG": DDPG,
         "TD3": TD3,
         "DQN": DQN}


def main():  # noqa: C901
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Directory name with model", type=str)
    args = parser.parse_args()
    model_name = glob.glob(f"{args.dir}/*.zip")[0]
    
    with open(f'{args.dir}/env_kwargs.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        env_kwargs = yaml.load(file, Loader=yaml.FullLoader)
    
    parsed = re.search("([a-zA-Z]+\-v\d+)\-([A-Z0-9]+)\-(\w+)\.zip", model_name)
    env_name = parsed.group(1)
    agent_name = parsed.group(2)
    team = parsed.group(3)
    import_gym(env_name)
    if env_kwargs is None:
        env = Monitor(gym.make(env_name))
    else:
        env = Monitor(gym.make(env_name, **env_kwargs))
    agent = MODEL[agent_name]
    model = agent.load(model_name[:-4])
    score = evaluate_policy(model, env, n_eval_episodes=100)
    
    leaderboard(agent = agent_name, 
                env = env_name,
                team = team, 
                mean = score[0], 
                std = score[1], 
                hashid = filehash(model_name), 
                file = "leaderboard.csv")
    
    
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

if __name__ == "__main__":
    main()
