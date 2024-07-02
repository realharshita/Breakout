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
initial_ball_speed_x = 5
initial_ball_speed_y = -5

paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 10

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
balls = [{"x": screen_width // 2, "y": screen_height // 2, "speed_x": initial_ball_speed_x, "speed_y": initial_ball_speed_y}]
score = 0

paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
brick_hit_sound = pygame.mixer.Sound("brick_hit.wav")
power_up_sound = pygame.mixer.Sound("power_up.wav")

game_state = "playing"  # possible states: "playing", "paused", "game_over"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if game_state == "playing":
                    game_state = "paused"
                elif game_state == "paused":
                    game_state = "playing"
            elif event.key == pygame.K_r and game_state == "game_over":
                current_level = 0
                load_level(levels[current_level])
                balls = [{"x": screen_width // 2, "y": screen_height // 2, "speed_x": initial_ball_speed_x, "speed_y": initial_ball_speed_y}]
                paddle_width = 100
                score = 0
                game_state = "playing"

    if game_state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += paddle_speed

        for ball in balls:
            ball["x"] += ball["speed_x"]
            ball["y"] += ball["speed_y"]

            if ball["x"] <= 0 or ball["x"] >= screen_width - ball_radius:
                ball["speed_x"] = -ball["speed_x"]
            if ball["y"] <= 0:
                ball["speed_y"] = -ball["speed_y"]
            if ball["y"] >= screen_height:
                balls.remove(ball)
                if not balls:
                    game_state = "game_over"

            paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
            ball_rect = pygame.Rect(ball["x"] - ball_radius, ball["y"] - ball_radius, ball_radius * 2, ball_radius * 2)

            if paddle_rect.colliderect(ball_rect):
                ball["speed_y"] = -ball["speed_y"]
                pygame.mixer.Sound.play(paddle_hit_sound)

            for row in bricks:
                for brick in row[:]:
                    if ball_rect.colliderect(brick):
                        ball["speed_y"] = -ball["speed_y"]
                        row.remove(brick)
                        score += 10
                        pygame.mixer.Sound.play(brick_hit_sound)
                        if random.random() < 0.1:
                            power_ups.append(create_power_up(brick.x, brick.y))

        for power_up in power_ups[:]:
            power_up["rect"].y += power_up_speed
            if power_up["rect"].colliderect(paddle_rect):
                pygame.mixer.Sound.play(power_up_sound)
                if power_up["type"] == "paddle_increase":
                    paddle_width += 50
                elif power_up["type"] == "extra_ball":
                    balls.append({"x": screen_width // 2, "y": screen_height // 2, "speed_x": initial_ball_speed_x, "speed_y": initial_ball_speed_y})
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
    for ball in balls:
        pygame.draw.circle(screen, ball_color, (ball["x"], ball["y"]), ball_radius)

    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, brick_color, brick)

    for power_up in power_ups:
        pygame.draw.rect(screen, power_up_color, power_up["rect"])

    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if game_state == "paused":
        font = pygame.font.SysFont(None, 55)
        text = font.render("Paused", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

    if game_state == "game_over":
        font = pygame.font.SysFont(None, 55)
        text = font.render("Game Over - Press R to Restart", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
