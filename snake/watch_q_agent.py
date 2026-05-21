import pygame
from settings import *
from snake_env import SnakeEnv
from q_learning_agent import QLearningAgent

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Podglad agenta")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

env = SnakeEnv()
agent = QLearningAgent()
agent.load("q_table.pkl")
agent.epsilon = 0.0

state = env.reset()

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    q_state = env.get_q_state()
    action = agent.choose_action(q_state)

    state,reward,done,info = env.step(action)

    if done:
        state = env.reset()

    screen.fill(BLACK)

    env.snake.draw(screen)
    env.food.draw(screen)

    score_text = font.render(f"Score: {info['score']}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()