import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the player
player_x = 100
player_y = 420
player_speed = 10

# Set up the platforms
platforms = [
    {"x": 300, "y": 200, "width": 50, "height": 10, "color": (255, 0, 0), "points": 1, "velocity": 2},
    {"x": 100, "y": 250, "width": 50, "height": 10, "color": (255, 255, 0), "points": 2, "velocity": 2},
    {"x": 500, "y": 300, "width": 50, "height": 10, "color": (255, 0, 0), "points": 1, "velocity": 2}
]

# Set up the score
score = 0

# Set up the difficulty
difficulty = 2

# Set up the stopwatch
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            difficulty += event.y
            if difficulty < 1:
                difficulty = 1
            for platform in platforms:
                platform["velocity"] = difficulty

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Collision with walls
    if player_x < 0:
        player_x = 0
    elif player_x + 70 > screen_width:
        player_x = screen_width - 70

    # Move the platforms
    for platform in platforms:
        platform["y"] += platform["velocity"]
        if platform["y"] > screen_height:
            platform["y"] = 0
            platform["x"] = random.randint(0, screen_width - 50)

    # Check for collision with the platforms
    for platform in platforms[:]:
        if (player_x < platform["x"] + platform["width"] and
            player_x + 70 > platform["x"] and
            player_y + 10 > platform["y"] and
            player_y < platform["y"] + platform["height"]):
            score += platform["points"]
            platform["y"] = 0
            platform["x"] = random.randint(0, screen_width - 50)

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, 70, 10))
    for platform in platforms:
        pygame.draw.rect(screen, platform["color"], (platform["x"], platform["y"], platform["width"], platform["height"]))
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render("Difficulty: " + str(difficulty), 1, (255, 255, 255))
    screen.blit(text, (10, 50))
    elapsed_time = (pygame.time.get_ticks() - start_time)
    minutes = elapsed_time // 60000
    seconds = (elapsed_time // 1000) % 60
    milliseconds = elapsed_time % 1000
    text = font.render("Time: " + str(minutes) + ":" + str(seconds).zfill(2) + "." + str(milliseconds).zfill(3), 1, (255, 255, 255))
    screen.blit(text, (10, 90))
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)