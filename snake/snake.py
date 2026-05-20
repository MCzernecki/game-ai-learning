import pygame
from settings import CELL_SIZE, GREEN, DARK_GREEN, WIDTH, HEIGHT, ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT

class Snake:
    def __init__(self):
        self.reset()

    def move(self, grow=False):
        head = self.get_next_head()

        self.body.insert(0, head)

        if not grow:
            self.body.pop()

    def draw(self, screen):
        for index, segment in enumerate(self.body):
            rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)

            if index == 0:
                pygame.draw.rect(screen, DARK_GREEN, rect)
            else:
                pygame.draw.rect(screen, GREEN, rect)

    def check_wall_collision(self):
        head = self.body[0]

        if head[0] < 0 or head[0] >= WIDTH:
            return True

        if head[1] < 0 or head[1] >= HEIGHT:
            return True

        return False

    def get_next_head(self):
        head = self.body[0].copy()
        head[0] += self.direction[0]
        head[1] += self.direction[1]
        return head

    def check_self_collision(self):
        head = self.body[0]

        if head in self.body[1:]:
            return True

        return False

    def set_direction(self, new_direction):
        opposite_direction = [-self.direction[0], -self.direction[1]]

        if new_direction != opposite_direction:
            self.direction = new_direction

    def set_direction_by_action(self, action):
        if action == ACTION_UP:
            self.set_direction([0, -CELL_SIZE])
        elif action == ACTION_DOWN:
            self.set_direction([0, CELL_SIZE])
        elif action == ACTION_LEFT:
            self.set_direction([-CELL_SIZE, 0])
        elif action == ACTION_RIGHT:
            self.set_direction([CELL_SIZE, 0])

    def reset(self):
        self.body = [
            [100, 100],
            [80, 100],
            [60, 100]
        ]
        self.direction = [CELL_SIZE, 0]