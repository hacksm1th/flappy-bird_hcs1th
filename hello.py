import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 400, 600
BIRD_SIZE = 50
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_VELOCITY = -5
GROUND_HEIGHT = 100
BACKGROUND_COLOR = (135, 206, 235)
FONT = pygame.font.Font(None, 36)


bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))


background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


ground_image = pygame.image.load("ground.png")
ground_image = pygame.transform.scale(ground_image, (WIDTH, GROUND_HEIGHT))


flap_sound = pygame.mixer.Sound("flap_sound.mp3")


pipe_sound = pygame.mixer.Sound("pipe_sound.mp3")

game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")


bird_rect = bird_image.get_rect(center=(100, HEIGHT // 2))
bird_velocity = 0


pipes = []
pipe_timer = 0


score = 0


game_over = False


clock = pygame.time.Clock()

def draw_ground():
    screen.blit(ground_image, (0, HEIGHT - GROUND_HEIGHT))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -10
                flap_sound.play()


    bird_velocity += 0.5
    bird_rect.centery += bird_velocity

   
    if bird_rect.colliderect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT):
        game_over = True
        bird_rect.centery = HEIGHT - GROUND_HEIGHT - BIRD_SIZE // 2
        game_over_sound.play()

    
    if pipe_timer == 0:
        pipe_height = random.randint(50, HEIGHT - PIPE_GAP - GROUND_HEIGHT - 50)
        top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, pipe_height)
        bottom_pipe = pygame.Rect(WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP - GROUND_HEIGHT)
        pipes.append((top_pipe, bottom_pipe))
        pipe_timer = 200  # Adjust this value to change pipe generation frequency

   
    for i, (top_pipe, bottom_pipe) in enumerate(pipes):
        top_pipe.x += PIPE_VELOCITY
        bottom_pipe.x += PIPE_VELOCITY
        if top_pipe.right < 0:
            pipes.pop(i)

        
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            game_over = True
            game_over_sound.play()

       
        if not top_pipe.colliderect(bird_rect) and top_pipe.right < bird_rect.left:
            score += 1
            pipe_sound.play()

    
    if pipe_timer > 0:
        pipe_timer -= 1

    
    screen.blit(background_image, (0, 0))

    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(screen, (0, 128, 0), top_pipe)
        pygame.draw.rect(screen, (0, 128, 0), bottom_pipe)

    draw_ground()
    screen.blit(bird_image, bird_rect)

   
    score_text = FONT.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

    
    clock.tick(60)


game_over_text = FONT.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(game_over_text, game_over_rect)
pygame.display.update()


pygame.time.delay(2000)


pygame.quit()
sys.exit()
