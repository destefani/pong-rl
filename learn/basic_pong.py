import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle settings
paddle_width, paddle_height = 10, 60
player_speed = 0
opponent_speed = 7

# Ball settings
ball_width, ball_height = 10, 10
ball_speed_x, ball_speed_y = 7, 7

# Create rectangles for ball and paddles
ball = pygame.Rect(
    SCREEN_WIDTH // 2 - ball_width // 2,
    SCREEN_HEIGHT // 2 - ball_height // 2,
    ball_width,
    ball_height,
)
player_paddle = pygame.Rect(
    SCREEN_WIDTH - 20,
    SCREEN_HEIGHT // 2 - paddle_height // 2,
    paddle_width,
    paddle_height,
)
opponent_paddle = pygame.Rect(
    10, SCREEN_HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height
)

# Game clock
clock = pygame.time.Clock()


def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_x *= random.choice((1, -1))
    ball_speed_y *= random.choice((1, -1))


# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    player_paddle.y += player_speed

    # Opponent AI
    if opponent_paddle.top < ball.y:
        opponent_paddle.y += opponent_speed
    if opponent_paddle.bottom > ball.y:
        opponent_paddle.y -= opponent_speed

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    # Ball goes out of the screen
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_restart()

    # Keeping paddles within the screen
    player_paddle.clamp_ip(screen.get_rect())
    opponent_paddle.clamp_ip(screen.get_rect())

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(
        screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT)
    )

    pygame.display.flip()
    clock.tick(60)
