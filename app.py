import pygame
import random
pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 900, 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# --- Fonts ---
font = pygame.font.SysFont("Arial", 40)
big_font = pygame.font.SysFont("Arial", 80)

clock = pygame.time.Clock()
FPS = 60

# --- Load images ---
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (120, 80))

pipe_img = pygame.image.load("pipe.png")
pipe_width = 80
pipe_img = pygame.transform.scale(pipe_img, (pipe_width, HEIGHT))

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

def game_loop():
    bird_x = 50
    bird_y = 250
    bird_width = 30
    bird_height = 30
    gravity = 0.5
    jump_strength = -10
    bird_velocity = 0

    pipe_gap = 150
    pipe_speed = 3

    # Multiple pipes
    pipes = []
    for i in range(3):
        pipe_x = WIDTH + i * 600
        pipe_height = random.randint(80, 260)
        pipes.append({"x": pipe_x, "height": pipe_height})

    score = 0
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength

        # --- Bird Movement ---
        bird_velocity += gravity
        bird_y += bird_velocity

        # --- Pipe Movement ---
        for pipe in pipes:
            pipe["x"] -= pipe_speed
            if pipe["x"] + pipe_width < 0:
                pipe["x"] = WIDTH
                pipe["height"] = random.randint(100, 300)
                score += 1

        # --- Collision Detection ---
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
        if bird_y <= 0 or bird_y + bird_height >= HEIGHT:
            return score

        for pipe in pipes:
            top_pipe_rect = pygame.Rect(pipe["x"], 0, pipe_width, pipe["height"])
            bottom_pipe_rect = pygame.Rect(pipe["x"], pipe["height"] + pipe_gap, pipe_width, HEIGHT)
            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                return score

        # --- Draw Everything ---
        window.blit(background_img, (0, 0))
        window.blit(bird_img, (bird_x, bird_y))

        for pipe in pipes:
            # Bottom pipe
            window.blit(pipe_img, (pipe["x"], pipe["height"] + pipe_gap))
            # Top pipe (flipped)
            top_pipe_img = pygame.transform.flip(pipe_img, False, True)
            window.blit(top_pipe_img, (pipe["x"], pipe["height"] - pipe_img.get_height()))

        # Score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_text, (10, 10))

        pygame.display.update()

def game_over_screen(score):
    while True:
        window.blit(background_img, (0, 0))

        over_text = big_font.render("GAME OVER", True, (0, 0, 0))
        score_text = font.render(f"Your Score: {score}", True, (0, 0, 0))
        restart_text = font.render("Press SPACE to Restart or ESC to Quit", True, (0, 0, 0))

        window.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//3))
        window.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        window.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, int(HEIGHT//1.5)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

# --- Main Loop ---
while True:
    final_score = game_loop()
    if final_score is None:
        break
    restart = game_over_screen(final_score)
    if not restart:
        break

pygame.quit()
