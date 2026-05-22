import torch
from snake_env import SnakeEnv
from dqn_model import DQN

env = SnakeEnv()

state = env.get_dqn_state()

state_tensor = torch.tensor(state, dtype=torch.float32)

model = DQN()
q_values = model(state_tensor)
print(q_values)