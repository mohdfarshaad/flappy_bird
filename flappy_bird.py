import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 288, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

GRAVITY = 0.25
FLAP = -5
PIPE_SPEED = 2
PIPE_GAP = 120

bg_img = pygame.image.load("sprites/background-day.png")
bird_img = pygame.image.load("sprites/yellowbird-midflap.png")
pipe_img = pygame.image.load("sprites/pipe-green.png")
pipe_top_img = pygame.transform.flip(pipe_img, False, True)

jump_sound = pygame.mixer.Sound("audio/wing.wav")
hit_sound = pygame.mixer.Sound("audio/hit.wav")
point_sound = pygame.mixer.Sound("audio/point.wav")

bird_rect = bird_img.get_rect(center=(50, HEIGHT // 2))
velocity = 0

pipe_x = WIDTH
pipe_height = random.randint(100, 280)
passed_pipe = False
score = 0
game_over = False

font = pygame.font.SysFont("Arial", 32)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_over:
                bird_rect.center = (50, HEIGHT // 2)
                velocity = 0
                pipe_x = WIDTH
                score = 0
                passed_pipe = False
                game_over = False
            else:
                velocity = FLAP
                jump_sound.play()

    if not game_over:
        velocity += GRAVITY
        bird_rect.y += velocity

        pipe_x -= PIPE_SPEED
        if pipe_x < -pipe_img.get_width():
            pipe_x = WIDTH
            pipe_height = random.randint(100, 280)
            passed_pipe = False

        top_rect = pipe_top_img.get_rect(bottomleft=(pipe_x, pipe_height))
        bottom_rect = pipe_img.get_rect(topleft=(pipe_x, pipe_height + PIPE_GAP))

        if not passed_pipe and pipe_x + pipe_img.get_width() < bird_rect.left:
            score += 1
            passed_pipe = True
            point_sound.play()

        if (
            bird_rect.colliderect(top_rect)
            or bird_rect.colliderect(bottom_rect)
            or bird_rect.bottom >= HEIGHT
            or bird_rect.top <= 0
        ):
            hit_sound.play()
            game_over = True

    screen.blit(bg_img, (0, 0))

    if not game_over:
        screen.blit(pipe_top_img, top_rect)
        screen.blit(pipe_img, bottom_rect)

    screen.blit(bird_img, bird_rect)

    score_surf = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, 40)))

    if game_over:
        over_surf = font.render("Press SPACE", True, (255, 255, 255))
        screen.blit(over_surf, over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()
    clock.tick(30)