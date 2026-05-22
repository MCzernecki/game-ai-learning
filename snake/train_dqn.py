from snake_env import SnakeEnv
from dqn_agent import DQNAgent
import os

env = SnakeEnv()
agent = DQNAgent()
if os.path.exists("dqn_model.pth"):
    agent.load("dqn_model.pth")
    agent.epsilon = 0.05
    print("DQN model loaded")

episodes = 1000

scores = []

for episode in range(episodes):
    print(f"Starting episode {episode + 1}")
    env.reset()

    state = env.get_dqn_state()

    done = False
    total_loss = 0

    while not done:
        action = agent.choose_action(state)
        _,reward, done, info = env.step(action)

        next_state = env.get_dqn_state()

        agent.remember(state, action, reward, next_state, done)
        loss = agent.train_from_memory()

        total_loss += loss
        state = next_state
    scores.append(info["score"])

    if agent.epsilon > agent.epsilon_min:
        agent.epsilon *= agent.epsilon_decay

        if agent.epsilon < agent.epsilon_min:
            agent.epsilon = agent.epsilon_min

    if (episode + 1) % 100 == 0:
        average_score = sum(scores[-100:]) / 100
        average_loss = total_loss / max(info["score"]+1,1)

        print(f"Episode {episode+1} "
              f"Average Score: {average_score:.2f} "
              f"Epsilon: {agent.epsilon:.3f} "
              f"Average Loss: {average_loss:.4f}")

agent.save("dqn_model.pth")
print("Training finished and DQN model saved")