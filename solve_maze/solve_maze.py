import sys
import argparse
import numpy as np
import pygame

from configs import cfg
from utils.get_maze import *
from environement.stochastic_environement import *
from algorithms.model_free.sarsa_algorithm import SARSA
from utils.display_utils import embed_mp4, DisplayVideo
from algorithms.model_free.q_learning_algorithm import QLearning
from algorithms.model_free.monte_carlo_algorithm import MonteCarlo
from algorithms.model_based.policy_iteration_algorithm import PolicyIteration
from maze_mid.cust_maze import MazeEnvCast5x5, MazeEnvCast15x15, MazeEnvCast25x25
from utils.human_mode import play_human

# 🔹 import our new visualization
from utils.policy_visualizer import visualize_policy

##############################################################
# the main file - run the chosen Algorithm OR play manually  #
##############################################################

env_dict = {
    5: StochasticEnv(MazeEnvCast5x5()),
    15: StochasticEnv(MazeEnvCast15x15()),
    25: StochasticEnv(MazeEnvCast25x25()),
}

algo_dict = {
    'PolicyIteration': (PolicyIteration, True),
    'MonteCarlo': (MonteCarlo, False),
    'QLearning': (QLearning, False),
    'SARSA': (SARSA, False),
}


def parse_args():
    parser = argparse.ArgumentParser(description='Solve Maze or Play Manually')
    parser.add_argument("-config_file", default="config.yaml", help="path to config file", type=str)
    parser.add_argument("--mode", choices=["AI", "HUMAN"], default="AI", help="Run with AI agent or play manually")
    parser.add_argument("--size", type=int, default=15, help="Maze size (5, 15, 25)")
    args, unknown = parser.parse_known_args()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(unknown)
    cfg.freeze()
    return args


def SetEnv(size):
    global env
    if 'env' in globals():
        env.close()
    env = env_dict.get(size)
    if env is None:
        raise ValueError("Invalid maze size")
    return env


def SetAlgorithm(algorithm_configs, env):
    algo_value = algo_dict.get(algorithm_configs.NAME)
    if algo_value is None:
        print(f"Algorithm name from config: {algorithm_configs.NAME}")
        raise ValueError("Invalid algorithm name")
    AlgoClass, is_model_based = algo_value
    algo = AlgoClass(env)
    algo.train()
    return algo, is_model_based






def main():
    args = parse_args()
    env = SetEnv(args.size)

    if args.mode == "HUMAN":
        play_human(env)
    else:
        # Run AI algorithm
        algo, is_model_based = SetAlgorithm(cfg.ALGORITHM, env)

        # 🔹 Show video (already in project)
        DisplayVideo(algo, env, f'{cfg.ALGORITHM.NAME}_{args.size}x{args.size}', is_model_based)


if __name__ == "__main__":
    main()
