import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Load the background image
background_image = pygame.image.load("background.jpg")

# Get the size of the background image
width, height = background_image.get_width(), background_image.get_height()

# Set the custom icon
icon_image = pygame.image.load("player.png")  # Replace "icon.png" with your own image filename
pygame.display.set_icon(icon_image)

# Calculate the desired window size while maintaining the aspect ratio
aspect_ratio = width / height
desired_height = 600  # Set the desired height of the window
desired_width = int(desired_height * aspect_ratio)

# Set up the game window
window = pygame.display.set_mode((desired_width, desired_height))
pygame.display.set_caption("Catch Me If You Can")

# Scale the background image to fit the window
background_image = pygame.transform.scale(background_image, (desired_width, desired_height))

# Load the player image
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))  # Scale the image to desired size

# Load the enemy image
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (40, 40))  # Scale the image to desired size

# Set up colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the player position and size
player_size = player_image.get_width()
player_x = desired_width // 2 - player_size // 2
player_y = desired_height // 2 - player_size // 2

# Set up the enemies
enemy_radius = 20
enemies = []
enemy_speed = 4

# Set the initial positions of the enemies in the four corners and the middle of each side
enemies.append({"x": enemy_radius, "y": enemy_radius, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})  # Top-left corner
enemies.append({"x": desired_width - enemy_radius, "y": enemy_radius, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})  # Top-right corner
enemies.append({"x": enemy_radius, "y": desired_height - enemy_radius, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})  # Bottom-left corner
enemies.append({"x": desired_width - enemy_radius, "y": desired_height - enemy_radius, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})  # Bottom-right corner
enemies.append({"x": desired_width // 2, "y": enemy_radius, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})  # Top-middle
enemies.append({"x": desired_width // 2, "y": desired_height - enemy_radius, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})  # Bottom-middle
enemies.append({"x": enemy_radius, "y": desired_height // 2, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})  # Left-middle
enemies.append({"x": desired_width - enemy_radius, "y": desired_height // 2, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})  # Right-middle

# Set up game variables
clock = pygame.time.Clock()
running = True
game_over = False

# Set up timer variables
start_time = pygame.time.get_ticks()
elapsed_time = 0

# Function to check pixel-perfect collision
def check_collision(obj1, obj2, pos1, pos2):
    rect1 = obj1.get_rect(topleft=pos1)
    rect2 = obj2.get_rect(topleft=pos2)
    overlap = rect1.clip(rect2)

    if overlap.width > 0 and overlap.height > 0:
        pixels1 = pygame.mask.from_surface(obj1)
        pixels2 = pygame.mask.from_surface(obj2)
        offset = (overlap.left - rect1.left, overlap.top - rect1.top)
        if pixels1.overlap(pixels2, offset):
            return True

    return False

# Game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < desired_width - player_size:
        player_x += 5
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= 5
    if keys[pygame.K_DOWN] and player_y < desired_height - player_size:
        player_y += 5

    # Clear the screen
    window.blit(background_image, (0, 0))

    # Draw the player
    window.blit(player_image, (player_x, player_y))

    # Update enemy positions and check for collisions
    for enemy in enemies:
        enemy_x = enemy["x"]
        enemy_y = enemy["y"]

        # Generate random directions for each enemy in each iteration
        if random.random() < 0.05:  # Adjust this value to control the randomness of direction changes
            enemy["dx"] = random.choice([-1, 1])
            enemy["dy"] = random.choice([-1, 1])

        enemy_x += enemy_speed * enemy["dx"]
        enemy_y += enemy_speed * enemy["dy"]

        # Check for collisions with the player
        if check_collision(player_image, enemy_image, (player_x, player_y), (enemy_x - enemy_radius, enemy_y - enemy_radius)):
            game_over = True
            break

        # Check for collisions with the screen edges and adjust position
        if enemy_x <= enemy_radius:
            enemy_x = enemy_radius + 1
            enemy["dx"] = random.choice([1])  # Reverse the x-direction
        elif enemy_x >= desired_width - enemy_radius:
            enemy_x = desired_width - enemy_radius - 1
            enemy["dx"] = random.choice([-1])  # Reverse the x-direction
        if enemy_y <= enemy_radius:
            enemy_y = enemy_radius + 1
            enemy["dy"] = random.choice([1])  # Reverse the y-direction
        elif enemy_y >= desired_height - enemy_radius:
            enemy_y = desired_height - enemy_radius - 1
            enemy["dy"] = random.choice([-1])  # Reverse the y-direction

        # Draw the enemy
        window.blit(enemy_image, (enemy_x - enemy_radius, enemy_y - enemy_radius))

        # Update the enemy position in the dictionary
        enemy["x"] = enemy_x
        enemy["y"] = enemy_y

    # Calculate the elapsed time
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000  # Convert to seconds

    # Display the elapsed time on the top center of the screen
    font = pygame.font.SysFont(None, 36)
    time_text = font.render(f"Time: {elapsed_time}s", True, RED)
    text_rect = time_text.get_rect(center=(desired_width // 2, 20))
    window.blit(time_text, text_rect)

    # Check if the player has died
    if game_over:
        # Display the "You died!" message in red
        game_over_text = font.render("You died!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(desired_width // 2, desired_height // 2))
        window.fill(BLACK)  # Fill the background with black
        window.blit(game_over_text, game_over_rect)
        
        # Display the scores
        scores = [elapsed_time]  # Add the current score
        with open("scores.txt", "a+") as file:
            file.seek(0)
            for line in file:
                scores.append(int(line.strip()))

        scores = sorted(scores, reverse=True)[:3]  # Get the top 3 scores
        scores_text = font.render("Scores", True, RED)
        scores_rect = scores_text.get_rect(center=(desired_width // 2, desired_height // 2 + 50))
        window.blit(scores_text, scores_rect)
        
        y_offset = 100
        for i, score in enumerate(scores):
            score_text = font.render(f"{i+1}. {score}s", True, RED)
            score_rect = score_text.get_rect(center=(desired_width // 2, desired_height // 2 + y_offset))
            window.blit(score_text, score_rect)
            y_offset += 50

        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second before closing the game
        running = False

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
