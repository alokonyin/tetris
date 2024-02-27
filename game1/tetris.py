import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 300, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Brick Game')

# Colors
BLACK = (0, 0, 0)
COLORS = [(0, 255, 255), (255, 165, 0), (0, 0, 255), (255, 255, 0), (128, 0, 128), (0, 128, 0), (255, 0, 0)]

# Define the tetromino shapes
tetrominos = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1],
     [0, 1, 0]],    # T
    [[0, 1, 1],
     [1, 1, 0]],    # S
    [[1, 1, 0],
     [0, 1, 1]],    # Z
    [[1, 1],
     [1, 1]],      # O
    [[1, 0, 0],
     [1, 1, 1]],    # J
    [[0, 0, 1],
     [1, 1, 1]]     # L
]

# Game variables
block_size = 30  # Size of the side of a tetris block
fall_speed = 0.3  # Speed at which the block falls

# Initial block position
block_x = screen_width // 2
block_y = 0

current_shape = tetrominos[random.randint(0, len(tetrominos) - 1)]  # Randomly select a shape
shape_color = COLORS[random.randint(0, len(COLORS) - 1)]

# Initialize the play area grid
grid_height = screen_height // block_size
grid_width = screen_width // block_size
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
grid_x = block_x // block_size
grid_y = block_y // block_size



clock = pygame.time.Clock()

def draw_block():
    for i, row in enumerate(current_shape):
        for j, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, shape_color, (block_x + j * block_size, block_y + i * block_size, block_size, block_size))

def rotate_shape():
    global current_shape, block_x  # Declare block_x and current_shape as globals at the start
    # Rotate the shape matrix clockwise
    current_shape = [list(row) for row in zip(*current_shape[::-1])]
    # Prevent the shape from going out of bounds after rotation
    if block_x + len(current_shape[0]) * block_size > screen_width:
        block_x = screen_width - len(current_shape[0]) * block_size

def check_collision(x, y, shape):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                # Check if the block is outside the grid bounds
                if x + j < 0 or x + j >= grid_width or y + i >= grid_height:
                    return True
                # Check if the block position is already filled in the grid
                elif grid[y + i][x + j] == 1:
                    return True
    return False


def place_block(x, y, shape, color):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == 1:
                grid[y+i][x+j] = 1  # Mark the grid position as filled

def check_clear_lines():
    global grid
    # Check from the bottom of the grid up
    y = grid_height - 1
    while y >= 0:
        if 0 not in grid[y]:  # This row is full
            del grid[y]  # Remove the row
            grid.insert(0, [0 for _ in range(grid_width)])  # Add an empty row at the top
            # No need to decrement y, as we want to check the new row that shifted down to this position
        else:
            y -= 1  # Move up to the next row

# Add global variables for score and level
score = 0
lines_cleared = 0
level = 1
fall_speed = 0.3  # Initial fall speed

# Modify the check_clear_lines function to update score and possibly level
def check_clear_lines():
    global grid, score, lines_cleared, level, fall_speed
    num_lines_cleared = 0  # Number of lines cleared in this call
    y = grid_height - 1
    while y >= 0:
        if 0 not in grid[y]:
            del grid[y]
            grid.insert(0, [0 for _ in range(grid_width)])
            num_lines_cleared += 1
        else:
            y -= 1
    if num_lines_cleared > 0:
        lines_cleared += num_lines_cleared
        # Update score, simple scoring system: 100 points per line
        score += num_lines_cleared * 100
        # Increase level after every 10 lines cleared
        if lines_cleared // 10 > level - 1:
            level += 1
            fall_speed *= 0.9  # Increase speed by 10%

# Check for game over condition in the game_loop, after a collision detection
def game_over():
    for x in range(grid_width):
        if grid[0][x] == 1:  # Check if any block is in the top row
            return True
    return False

# Update game_loop to check for game over
def game_loop():
    global block_y, current_shape, block_x
    screen.fill(BLACK)
    draw_block()

    grid_x = int(block_x // block_size)
    grid_y = int(block_y // block_size)

    if not check_collision(grid_x, grid_y + 1, current_shape):
        block_y += fall_speed
    else:
        place_block(grid_x, grid_y, current_shape, shape_color)
        if game_over():
            print(f"Game Over! Final Score: {score}, Level: {level}")
            pygame.quit()
            sys.exit()
        check_clear_lines()
        reset_game()

    pygame.display.flip()

# Ensure reset_game doesn't need modifications for game over
# But you might want to reset score and level if you add a way to restart the game

# Main game loop remains unchanged


def reset_game():
    global block_x, block_y, current_shape, shape_color
    block_x = screen_width // 2 - (len(current_shape[0]) * block_size) // 2
    block_y = 0
    current_shape = tetrominos[random.randint(0, len(tetrominos) - 1)]
    shape_color = COLORS[random.randint(0, len(COLORS) - 1)]
    
    if check_game_over():
        # Game over logic
        print("Game Over!")
        pygame.quit()
        sys.exit()  # For simplicity, this exits the game. You could implement a restart feature here.

# This is a conceptual example and needs to be integrated into your Pygame event loop for actual use
def game_over_prompt():
    choice = input("Game Over! Restart? (y/n): ")
    if choice.lower() == 'y':
        main()  # Assuming your main game loop is encapsulated in this function
    else:
        pygame.quit()
        sys.exit()


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Rotate shape on up arrow key press
                rotate_shape()

    game_loop()
    clock.tick(60)  #

