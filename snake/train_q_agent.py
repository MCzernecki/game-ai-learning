from snake_env import SnakeEnv
from q_learning_agent import QLearningAgent
import os
import csv

env = SnakeEnv()
agent = QLearningAgent()
if os.path.exists("q_table.pkl"):
    agent.load("q_table.pkl")
    agent.epsilon = 0.05
    print("Model loaded")

episodes = 1000

scores = []
stats = []

for episode in range(episodes):
    env.reset()
    state = env.get_q_state()
    done = False

    while not done:
        action = agent.choose_action(state)
        _, reward, done, info = env.step(action)

        next_state = env.get_q_state()

        agent.learn(state, action, reward, next_state, done)
        state = next_state

    scores.append(info["score"])

    if agent.epsilon > 0.01:
        agent.epsilon *= 0.995

    if (episode + 1) % 100 == 0:
        average_score = sum(scores[-100:]) / 100
        stats.append([
            episode + 1,
            info["score"],
            average_score,
            agent.epsilon
        ])

        print(
            f"Episode: {episode + 1}, "
            f"Average Score: {average_score:.2f}, "
            f"Epsilon: {agent.epsilon:.3f}"
        )

with open("training_stats.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Episode", "Score", "Average Score", "Epsilon"])
    writer.writerows(stats)

agent.save("q_table.pkl")

print("Training finished and model saved")