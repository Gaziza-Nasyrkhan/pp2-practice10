import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
TILE = 20  # size of one grid cell

def create_background(screen, width, height):
        colors = [(255, 255, 255), (212, 212, 212)]
        y = 0
        while y < height:
                x = 0
                while x < width:
                        row = y // TILE
                        col = x // TILE
                        # draw chess-like grid
                        pygame.draw.rect(screen, colors[(row + col) % 2],pygame.Rect(x, y, TILE, TILE))
                        x += TILE
                y += TILE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
GRAY = (100,100,100)

font = pygame.font.SysFont("Arial", 34)

def generate_walls(level):
    walls = []
    f = open("levels/level{}.txt".format(level), "r")
    row = -1
    col = -1
    for line in f:
        row = row + 1
        col = -1
        for c in line:
            col = col + 1
            if c == '#':
                # add wall blocks from file
                walls.append((col * TILE, row * TILE))
    f.close()
    return walls

def generate_food(snake, walls):
    while True:
        x = random.randrange(0, WIDTH, TILE)
        y = random.randrange(0, HEIGHT, TILE)

        # ensure food not on snake or wall
        if (x, y) not in snake and (x, y) not in walls:
            return (x, y)

def reset_game():
    snake = [(100,100), (80,100), (60,100)]
    dx, dy = TILE, 0  # initial movement
    level = 1
    walls = generate_walls(level)
    food = generate_food(snake, walls)
    score = 0
    speed = 5
    return snake, dx, dy, food, score, level, speed, walls

snake, dx, dy, food, score, level, speed, walls = reset_game()
game_over = False

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # control direction (no reverse allowed)
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -TILE
            if event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, TILE
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -TILE, 0
            if event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = TILE, 0

    if not game_over:
        # move snake head
        head = (snake[0][0] + dx, snake[0][1] + dy)

        # collision checks
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            game_over = True

        if head in snake:
            game_over = True

        if head in walls:
            game_over = True

        snake.insert(0, head)

        if head == food:
            score += 1

            # level up every 3 points
            if score != 0 and score % 3 == 0:
                level += 1
                speed += 1
                walls = generate_walls(level)

            food = generate_food(snake, walls)
        else:
            snake.pop()

        create_background(screen, 600,600)

    # draw snake
    for s in snake:
        pygame.draw.rect(screen, GREEN, (*s, TILE, TILE))

    pygame.draw.rect(screen, RED, (*food, TILE, TILE))

    # draw walls
    for w in walls:
        pygame.draw.rect(screen, GRAY, (*w, TILE, TILE))

    text = font.render(f"Score: {score} Level: {level}", True, BLACK)
    screen.blit(text, (10, 10))

    if game_over:
        screen.fill(RED)
        over = font.render("GAME OVER! Press R FOR RESTART", True, BLACK)
        screen.blit(over, (70, 260))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # restart game
            snake, dx, dy, food, score, level, speed, walls = reset_game()
            game_over = False

    pygame.display.flip()
    clock.tick(speed)  # speed increases with level

pygame.quit()