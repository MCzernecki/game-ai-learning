import random
from settings import ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT

class QLearningAgent:
    def __init__(self):
        self.actions = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

        self.q_table = {}

        self.learning_rate = 0.1
        self.discount_rate = 0.9
        self.epsilon = 1.0

    def get_q_values(self, state):
        if state not in self.q_table:
            self.q_table[state] = { ACTION_UP: 0, ACTION_DOWN: 0, ACTION_LEFT: 0, ACTION_RIGHT: 0}
        return self.q_table[state]

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = self.get_q_values(state)
            return max(q_values, key=q_values.get)

    def learn(self, state, action, reward, next_state, done):
        q_values = self.get_q_values(state)
        current_q = q_values[action]

        next_q_values = self.get_q_values(next_state)
        max_next_q = max(next_q_values.values())

        if done:
            target_q = reward
        else:
            target_q = reward + self.discount_rate * max_next_q

        new_q = current_q + self.learning_rate * (target_q - current_q)
        q_values[action] = new_q

    def save(self, filename):
        import pickle

        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, filename):
        import pickle

        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)