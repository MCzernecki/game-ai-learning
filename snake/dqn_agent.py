import random
import torch
import torch.nn as nn
import torch.optim as optim
from dqn_model import DQN
from replay_memory import ReplayMemory

class DQNAgent:
    def __init__(self):
        self.model = DQN()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        self.criterion = nn.MSELoss()

        self.gamma = 0.9

        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        self.memory = ReplayMemory()
        self.batch_size = 64
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 3)

        state_tensor = torch.tensor(state, dtype=torch.float32)

        with torch.no_grad():
            q_values = self.model(state_tensor)

        return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

    def train_from_memory(self):
        if len(self.memory) < self.batch_size:
            return 0

        batch = self.memory.sample(self.batch_size)

        states = []
        actions = []
        rewards = []
        next_states = []
        dones = []

        for state, action, reward, next_state, done in batch:
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            dones.append(done)

        states_tensor = torch.tensor(states, dtype=torch.float32)
        actions_tensor = torch.tensor(actions, dtype=torch.long)
        rewards_tensor = torch.tensor(rewards, dtype=torch.float32)
        next_states_tensor = torch.tensor(next_states, dtype=torch.float32)
        dones_tensor = torch.tensor(dones, dtype=torch.bool)

        predicted_q_values = self.model(states_tensor)

        predicted_action_q_values = predicted_q_values.gather(1, actions_tensor.unsqueeze(1)).squeeze(1)

        with torch.no_grad():
            next_q_values = self.model(next_states_tensor)
            max_next_q_values = torch.max(next_q_values, dim=1)[0]
            target_q_values = rewards_tensor + self.gamma * max_next_q_values
            target_q_values = torch.where(
                dones_tensor,
                rewards_tensor,
                target_q_values
            )

        loss = self.criterion(predicted_action_q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def train_step(self, state, action, reward, next_state, done):
        state_tensor = torch.tensor(state, dtype=torch.float32)
        next_state_tensor = torch.tensor(next_state, dtype=torch.float32)

        predicted_q_values = self.model(state_tensor)
        target_q_values = predicted_q_values.clone().detach()

        if done:
            target_q_values[action] = reward
        else:
            with torch.no_grad():
                next_q_values = self.model(next_state_tensor)
                max_next_q = torch.max(next_q_values).item()
            target_q_values[action] = reward + self.gamma * max_next_q

        loss = self.criterion(predicted_q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def save(self, filename):
        torch.save(self.model.state_dict(), filename)

    def load(self, filename):
        self.model.load_state_dict(torch.load(filename))