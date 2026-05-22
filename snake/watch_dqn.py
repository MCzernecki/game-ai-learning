import pygame
from settings import *
from snake_env import SnakeEnv
from dqn_agent import DQNAgent

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Podglad agenta DQN")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

env = SnakeEnv()

agent = DQNAgent()
agent.load("dqn_model.pth")

agent.epsilon = 0.0

env.reset()

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    state = env.get_dqn_state()

    action = agent.choose_action(state)

    _, reward, done, info = env.step(action)

    if done:
        env.reset()

    screen.fill(BLACK)

    env.snake.draw(screen)
    env.food.draw(screen)

    score_text = font.render(f"Score: {info['score']}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()