import random
from settings import ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT

class RandomBot:
    def choose_action(self, state):
        return random.choice([ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT])