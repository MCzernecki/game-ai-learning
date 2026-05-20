import random
import pygame
from settings import CELL_SIZE, WIDTH, HEIGHT, RED, TOP_MARGIN


class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self, snake_body=None):
        while True:
            x= random.randrange(0, WIDTH, CELL_SIZE)
            y= random.randrange(TOP_MARGIN, HEIGHT, CELL_SIZE)
            position = [x, y]

            if snake_body is None or position not in snake_body:
                return position

    def draw(self, screen):
        center_x = self.position[0] + CELL_SIZE // 2
        center_y = self.position[1] + CELL_SIZE // 2
        radius = CELL_SIZE // 2
        pygame.draw.circle(screen, RED, (center_x, center_y), radius)
