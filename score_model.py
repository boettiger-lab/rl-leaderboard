from stable_baselines3 import A2C, PPO, SAC, DDPG, TD3, DQN
import gym_fishing
import gym_conservation
import gym
import os
import re
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

model_obj = "cache/fishing-v1-A2C-team_vanilla.zip"

parsed = re.search("([a-zA-Z]+\-v\d+)\-([A-Z0-9]+)\-(\w+)\.zip", model_obj)
env_name = parsed.group(1)
agent_name = parsed.group(2)
team = parsed.group(3)
env = Monitor(gym.make(env_name))
agent = MODEL[agent_name]
model = agent.load(model_obj)
score = evaluate_policy(model, env, n_eval_episodes=100)

leaderboard(agent = agent, 
            env = env_name,
            team = team, 
            mean = score[0], 
            std = score[1], 
            hashid = filehash(model_obj), 
            file = "leaderboard.csv")

