import pygame
import sys
import random 
import time
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer")

blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
white = (255,255,255)

score = 0
speed = 4
coins = 0

width = 400
height = 600

# Font setup
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

pygame.mixer.init()

# Load images and resize
background = pygame.image.load("AnimatedStreet.png")
player = pygame.transform.scale(pygame.image.load("Player.png"), (60,100))
enemy = pygame.transform.scale(pygame.image.load("Enemy.png"),(60,100))
coin = pygame.transform.scale(pygame.image.load("coiin.png"), (30,30))

crash = pygame.mixer.Sound("crash.mp3")

# Get rectangles for positioning and collision
playerrect = player.get_rect()
playerrect.center = (160,520)

enemyrect = enemy.get_rect()
enemyrect.center = (random.randint(40, width - 40),0)

coinrect = coin.get_rect()
coinrect.center = (random.randint(40, width - 40), -100)

# Custom event to increase speed over time
inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

def move_player():
    pressed_keys = pygame.key.get_pressed()
    # Move left/right within screen limits
    if pressed_keys[K_LEFT] and playerrect.left > 0:
        playerrect.move_ip(-5,0)

    if pressed_keys[K_RIGHT] and playerrect.right < width:
        playerrect.move_ip(5,0)

def move_enemy():
    global score
    enemyrect.move_ip(0, speed)

    # Reset enemy and increase score when it goes off screen
    if enemyrect.top > height:
        score += 1
        enemyrect.center = (random.randint(40, width - 40), 0)

def move_coin():
    global coins
    coinrect.move_ip(0, speed-2)

    # Respawn coin when it goes off screen
    if coinrect.top > height:
        coinrect.center = (random.randint(40, width -40), -50)

    # Collect coin on collision
    if playerrect.colliderect(coinrect):
        coins += 1
        coinrect.center = (random.randint(40, width - 40), -50)

# Background music
backgroundsound = pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play()

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == inc_speed:
            speed += 0.5  # gradually increase difficulty
        
    screen.blit(background, (0,0))

    # Display score and coins
    scoretext = font_small.render("Score: " + str(score), True, black)
    screen.blit(scoretext, (10,10))

    coin_text = font_small.render("Coins: " + str(coins), True, black)
    screen.blit(coin_text, (280,10))

    move_player()
    move_enemy()
    move_coin()

    screen.blit(player, playerrect)
    screen.blit(enemy, enemyrect)
    screen.blit(coin, coinrect)

    # Collision with enemy -> game over
    if playerrect.colliderect(enemyrect):
        pygame.mixer.music.pause()
        crash.play()

        screen.fill(red)
        screen.blit(game_over, (30,250))
        pygame.display.update()
        
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    clock.tick(60)