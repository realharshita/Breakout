import pygame
import sys
import random

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout Game")

paddle_width = 100
paddle_height = 20
paddle_color = (255, 255, 255)
paddle_speed = 10

ball_radius = 10
ball_color = (255, 255, 255)
ball_speed_x = 5
ball_speed_y = -5

paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 10
ball_x = screen_width // 2
ball_y = screen_height // 2

brick_width = 75
brick_height = 20
brick_color = (255, 0, 0)
brick_padding = 10
power_up_width = 20
power_up_height = 20
power_up_color = (0, 255, 0)
power_up_speed = 5

levels = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    ],
    [
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
    ]
]

current_level = 0
bricks = []

def load_level(level):
    global bricks
    bricks = []
    for row_index, row in enumerate(level):
        brick_row = []
        for col_index, brick in enumerate(row):
            if brick == 1:
                brick_x = col_index * (brick_width + brick_padding) + brick_padding
                brick_y = row_index * (brick_height + brick_padding) + brick_padding
                brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
                brick_row.append(brick_rect)
        bricks.append(brick_row)

def create_power_up(x, y):
    power_up_type = random.choice(["paddle_increase", "extra_ball"])
    power_up_rect = pygame.Rect(x, y, power_up_width, power_up_height)
    return {"rect": power_up_rect, "type": power_up_type}

load_level(levels[current_level])
power_ups = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_x <= 0 or ball_x >= screen_width - ball_radius:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y
    if ball_y >= screen_height:
        ball_x = screen_width // 2
        ball_y = screen_height // 2
        ball_speed_x = 5
        ball_speed_y = -5

    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)

    if paddle_rect.colliderect(ball_rect):
        ball_speed_y = -ball_speed_y

    for row in bricks:
        for brick in row[:]:
            if ball_rect.colliderect(brick):
                ball_speed_y = -ball_speed_y
                row.remove(brick)
                if random.random() < 0.1:
                    power_ups.append(create_power_up(brick.x, brick.y))

    for power_up in power_ups[:]:
        power_up["rect"].y += power_up_speed
        if power_up["rect"].colliderect(paddle_rect):
            if power_up["type"] == "paddle_increase":
                paddle_width += 50
            elif power_up["type"] == "extra_ball":
                pass
            power_ups.remove(power_up)
        elif power_up["rect"].y > screen_height:
            power_ups.remove(power_up)

    if all(len(row) == 0 for row in bricks):
        current_level += 1
        if current_level >= len(levels):
            current_level = 0
        load_level(levels[current_level])

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, brick_color, brick)

    for power_up in power_ups:
        pygame.draw.rect(screen, power_up_color, power_up["rect"])

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
