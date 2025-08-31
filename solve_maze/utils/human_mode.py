import pygame
import numpy as np

# Map arrow keys to actions (assuming 0:UP, 1:RIGHT, 2:DOWN, 3:LEFT)
KEY_TO_ACTION = {
    pygame.K_UP: 0,
    pygame.K_RIGHT: 1,
    pygame.K_DOWN: 2,
    pygame.K_LEFT: 3,
}

def play_human(env):
    pygame.init()
    state = env.reset()
    done = False
    total_reward = 0
    running = True

    print("🎮 Use arrow keys to play the maze. Press ESC to quit.")

    while running and not done:
        # render EVERY FRAME (like QLearning/SARSA)
        env.render()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

                if event.key in KEY_TO_ACTION:
                    action = KEY_TO_ACTION[event.key]
                    next_state, reward, done, _ = env.step(action)
                    total_reward += reward
                    state = next_state.copy()

                    print(f"➡️ Action: {action}, Reward: {reward}, Done: {done}")

                    if done:
                        print(f"✅ Episode finished! Total reward: {total_reward}")
                        running = False
                        break

    pygame.quit()
