from settings import ACTION_UP, ACTION_LEFT, ACTION_RIGHT, ACTION_DOWN, CELL_SIZE, WIDTH, HEIGHT, TOP_MARGIN, MAX_MOVES_WITHOUT_FOOD
from snake import Snake
from food import Food

class SnakeEnv:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.moves_without_food = 0
        self.done = False

    def reset(self):
        self.snake.reset()
        self.food.position = self.food.random_position(self.snake.body)
        self.score = 0
        self.moves_without_food = 0
        self.done = False

        return  self.get_state()

    def get_state(self):
        head = self.snake.body[0]

        possible_moves = {
            ACTION_UP: [head[0], head[1] - CELL_SIZE],
            ACTION_DOWN: [head[0], head[1] + CELL_SIZE],
            ACTION_LEFT: [head[0] - CELL_SIZE, head[1]],
            ACTION_RIGHT: [head[0] + CELL_SIZE, head[1]]
        }

        danger = {}

        for action, position in possible_moves.items():
            x = position[0]
            y = position[1]

            wall_collision = x < 0 or x >= WIDTH or y < TOP_MARGIN or y >= HEIGHT
            self_collision = position in self.snake.body

            danger[action] = wall_collision or self_collision

        return {
            "head_x": head[0],
            "head_y": head[1],
            "food_x": self.food.position[0],
            "food_y": self.food.position[1],
            "direction_x": self.snake.direction[0],
            "direction_y": self.snake.direction[1],
            "score": self.score,
            "moves_without_food": self.moves_without_food,
            "danger": danger
        }

    def get_q_state(self):
        state = self.get_state()

        head_x = state["head_x"]
        head_y = state["head_y"]
        food_x = state["food_x"]
        food_y = state["food_y"]
        danger = state["danger"]

        return (
            danger[ACTION_UP],
            danger[ACTION_DOWN],
            danger[ACTION_LEFT],
            danger[ACTION_RIGHT],

            food_y < head_y,
            food_y > head_y,
            food_x < head_x,
            food_x > head_x
        )

    def get_dqn_state(self):
        state = self.get_q_state()

        return [
            int(state[0]),
            int(state[1]),
            int(state[2]),
            int(state[3]),
            int(state[4]),
            int(state[5]),
            int(state[6]),
            int(state[7])
        ]

    def step(self, action):
        if self.done:
            return self.get_state(), 0, self.done, {
                "score": self.score,
            }
        self.snake.set_direction_by_action(action)

        old_distance = abs(self.snake.body[0][0] - self.food.position[0]) + abs(self.snake.body[0][1] - self.food.position[1])

        grow = self.snake.get_next_head() == self.food.position
        self.snake.move(grow)
        new_distance = abs(self.snake.body[0][0] - self.food.position[0]) + abs(self.snake.body[0][1] - self.food.position[1])
        self.moves_without_food += 1
        reward = 0
        if new_distance < old_distance:
            reward += 0.2
        else:
            reward -= 0.2

        if grow:
            self.score += 1
            self.moves_without_food = 0
            self.food.position = self.food.random_position(self.snake.body)
            reward = 10
        if self.snake.check_wall_collision() or self.snake.check_self_collision():
            self.done = True
            reward = -10
        if self.moves_without_food > MAX_MOVES_WITHOUT_FOOD:
            self.done = True
            reward = -10

        return self.get_state(), reward, self.done, {
            "score": self.score,
        }