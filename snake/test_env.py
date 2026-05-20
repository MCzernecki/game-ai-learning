from snake_env import SnakeEnv
from smart_bot import SmartBot

env = SnakeEnv()
bot = SmartBot()

games_count = 100

scores = []

for game in range(games_count):
    state = env.reset()
    done = False

    while not done:
        action = bot.choose_action(state)
        state, reward, done, info = env.step(action)

    scores.append(info['score'])

average_score = sum(scores) / len(scores)
best_score = max(scores)
worst_score = min(scores)

print("Games: ", games_count)
print("Average Score: ", average_score)
print("Best Score: ", best_score, " Worst Score: ", worst_score, "")