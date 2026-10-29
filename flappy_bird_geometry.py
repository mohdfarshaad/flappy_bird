
import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 288, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Shapes Only")
clock = pygame.time.Clock()

# Game settings
GRAVITY = 0.25
FLAP = -5
PIPE_SPEED = 2
PIPE_GAP = 130
PIPE_WIDTH = 50
GROUND_HEIGHT = 40

# Colors
SKY = (112, 197, 206)
WHITE = (255, 255, 255)
GREEN = (83, 183, 55)
DARK_GREEN = (50, 145, 45)
YELLOW = (255, 220, 40)
ORANGE = (255, 150, 20)
BLACK = (30, 30, 30)
GROUND = (222, 216, 149)
GROUND_LINE = (190, 180, 110)

# Bird
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 12
velocity = 0

# Pipes
pipe_x = WIDTH
pipe_height = random.randint(100, 280)
passed_pipe = False

score = 0
game_over = False
started = False

font = pygame.font.SysFont("Arial", 28, bold=True)
small_font = pygame.font.SysFont("Arial", 16)

def draw_background():
    screen.fill(SKY)

    # Sun
    pygame.draw.circle(screen, (255, 235, 120), (235, 65), 25)

    # Clouds
    for x, y in [(45, 90), (175, 145), (260, 210)]:
        pygame.draw.circle(screen, WHITE, (x, y), 13)
        pygame.draw.circle(screen, WHITE, (x + 13, y - 6), 17)
        pygame.draw.circle(screen, WHITE, (x + 28, y), 12)

    # Ground
    pygame.draw.rect(
        screen, GROUND,
        (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
    )
    pygame.draw.line(
        screen, GROUND_LINE,
        (0, HEIGHT - GROUND_HEIGHT),
        (WIDTH, HEIGHT - GROUND_HEIGHT), 3
    )

    # Ground pattern
    for x in range(0, WIDTH, 24):
        pygame.draw.line(
            screen, GROUND_LINE,
            (x, HEIGHT - 20),
            (x + 12, HEIGHT - 20), 2
        )

def draw_pipe(x, height):
    bottom_y = height + PIPE_GAP
    ground_y = HEIGHT - GROUND_HEIGHT

    # Top pipe
    pygame.draw.rect(
        screen, GREEN,
        (x, 0, PIPE_WIDTH, height - 10)
    )
    pygame.draw.rect(
        screen, DARK_GREEN,
        (x, 0, 7, height - 10)
    )
    pygame.draw.rect(
        screen, GREEN,
        (x - 4, height - 20, PIPE_WIDTH + 8, 20)
    )
    pygame.draw.rect(
        screen, DARK_GREEN,
        (x - 4, height - 20, 7, 20)
    )

    # Bottom pipe
    pygame.draw.rect(
        screen, GREEN,
        (x, bottom_y + 10, PIPE_WIDTH, ground_y - bottom_y - 10)
    )
    pygame.draw.rect(
        screen, DARK_GREEN,
        (x, bottom_y + 10, 7, ground_y - bottom_y - 10)
    )
    pygame.draw.rect(
        screen, GREEN,
        (x - 4, bottom_y, PIPE_WIDTH + 8, 20)
    )
    pygame.draw.rect(
        screen, DARK_GREEN,
        (x - 4, bottom_y, 7, 20)
    )

def draw_bird(x, y):
    # Body
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), bird_radius)

    # Wing
    pygame.draw.ellipse(
        screen, ORANGE,
        (int(x - 10), int(y), 13, 8)
    )

    # Eye
    pygame.draw.circle(screen, WHITE, (int(x + 5), int(y - 5)), 5)
    pygame.draw.circle(screen, BLACK, (int(x + 7), int(y - 5)), 2)

    # Beak
    pygame.draw.polygon(
        screen, ORANGE,
        [
            (int(x + 10), int(y)),
            (int(x + 21), int(y + 3)),
            (int(x + 10), int(y + 6))
        ]
    )

def reset_game():
    global bird_y, velocity, pipe_x, pipe_height
    global passed_pipe, score, game_over, started

    bird_y = HEIGHT // 2
    velocity = 0
    pipe_x = WIDTH
    pipe_height = random.randint(100, 280)
    passed_pipe = False
    score = 0
    game_over = False
    started = True

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key in (pygame.K_SPACE, pygame.K_UP):
                if game_over:
                    reset_game()
                else:
                    started = True
                    velocity = FLAP

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            else:
                started = True
                velocity = FLAP

    if started and not game_over:
        velocity += GRAVITY
        bird_y += velocity

        pipe_x -= PIPE_SPEED

        if pipe_x < -PIPE_WIDTH:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 280)
            passed_pipe = False

        bird_rect = pygame.Rect(
            bird_x - bird_radius,
            int(bird_y) - bird_radius,
            bird_radius * 2,
            bird_radius * 2
        )

        top_rect = pygame.Rect(
            pipe_x, 0, PIPE_WIDTH, pipe_height
        )

        bottom_rect = pygame.Rect(
            pipe_x,
            pipe_height + PIPE_GAP,
            PIPE_WIDTH,
            HEIGHT - GROUND_HEIGHT - (pipe_height + PIPE_GAP)
        )

        if not passed_pipe and pipe_x + PIPE_WIDTH < bird_x:
            score += 1
            passed_pipe = True

        if (
            bird_rect.colliderect(top_rect)
            or bird_rect.colliderect(bottom_rect)
            or bird_y + bird_radius >= HEIGHT - GROUND_HEIGHT
            or bird_y - bird_radius <= 0
        ):
            game_over = True

    draw_background()

    if started:
        draw_pipe(pipe_x, pipe_height)

    draw_bird(bird_x, bird_y)

    # Score
    score_text = font.render(str(score), True, WHITE)
    screen.blit(
        score_text,
        score_text.get_rect(center=(WIDTH // 2, 40))
    )

    # Start screen
    if not started:
        title = font.render("Flappy Bird", True, WHITE)
        instruction = small_font.render(
            "Press SPACE or click to fly", True, WHITE
        )
        screen.blit(
            title,
            title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25))
        )
        screen.blit(
            instruction,
            instruction.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 15))
        )

    # Game over screen
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        over_text = font.render("Game Over", True, WHITE)
        restart_text = small_font.render(
            "Press SPACE or click to restart", True, WHITE
        )

        screen.blit(
            over_text,
            over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        )
        screen.blit(
            restart_text,
            restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        )

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
