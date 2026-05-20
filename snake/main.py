import pygame
from settings import *
from snake import Snake
from food import Food
from smart_bot import SmartBot

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

snake = Snake()
food = Food()
bot = SmartBot()
use_bot = False
score = 0
game_over = False
paused = False
game_started = False
high_score = 0
moves_without_food = 0

def reset_game():
    snake.reset()
    food.position = food.random_position(snake.body)
    return 0, False, 0

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_game():
    screen.fill(BLACK)
    draw_grid()

    snake.draw(screen)
    food.draw(screen)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 30))
    bot_text = font.render(f"Bot: {'ON' if use_bot else 'OFF'}", True, WHITE)
    screen.blit(bot_text, (10, 60))

    if game_over:
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (300, 300))

    if paused and not game_over:
        paused_text = font.render("Paused", True, WHITE)
        screen.blit(paused_text, (300, 300))

    if not game_started:
        start_text = font.render("Press SPACE to start", True, WHITE)
        screen.blit(start_text, (300, 300))


    pygame.display.update()

def update_game():
    global score, game_over, high_score, moves_without_food

    if game_started and not game_over and not paused:
        grow = snake.get_next_head() == food.position
        snake.move(grow)
        moves_without_food += 1
        if grow:
            score += 1
            moves_without_food = 0
            if score > high_score:
                high_score = score
            food.position = food.random_position(snake.body)
        if snake.check_wall_collision() or snake.check_self_collision():
            game_over = True
        if moves_without_food > MAX_MOVES_WITHOUT_FOOD:
            game_over = True

def get_game_state():
    head = snake.body[0]

    possible_moves = {
        ACTION_UP: (head[0], head[1] - CELL_SIZE),
        ACTION_DOWN: (head[0], head[1] + CELL_SIZE),
        ACTION_LEFT: (head[0] - CELL_SIZE, head[1]),
        ACTION_RIGHT: (head[0] + CELL_SIZE, head[1])
    }

    danger = {}

    for action, position in possible_moves.items():
        x = position[0]
        y = position[1]

        wall_collision = x < 0 or x >= WIDTH or y < TOP_MARGIN or y >= HEIGHT
        self_collision = position in snake.body

        danger[action] = wall_collision or self_collision

    return {
        "head_x": head[0],
        "head_y": head[1],
        "food_x": food.position[0],
        "food_y": food.position[1],
        "direction_x": snake.direction[0],
        "direction_y": snake.direction[1],
        "score": score,
        "moves_without_food": moves_without_food,
        "danger": danger
    }

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.set_direction_by_action(ACTION_UP)
            if event.key == pygame.K_DOWN:
                snake.set_direction_by_action(ACTION_DOWN)
            if event.key == pygame.K_LEFT:
                snake.set_direction_by_action(ACTION_LEFT)
            if event.key == pygame.K_RIGHT:
                snake.set_direction_by_action(ACTION_RIGHT)
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                elif game_over:
                    score, game_over, moves_without_food = reset_game()
            if event.key == pygame.K_p and not game_over and game_started:
                paused = not paused
            if event.key == pygame.K_b:
                use_bot = not use_bot

    if use_bot and game_started and not game_over and not paused:
        state = get_game_state()
        action = bot.choose_action(state)
        snake.set_direction_by_action(action)

    update_game()
    draw_game()

pygame.quit()