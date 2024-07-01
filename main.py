import pygame
import sys

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

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, paddle_color, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
