import pygame
import time
import math
import sauvegarde_
import ast

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY=(200,200,200)
COLORFUL= (100, 191, 255)

# Initialize Pygame
pygame.init()

# Set the dimensions of the grid and cells
grid_size = 9
cell_size = 50
grid_width = grid_height = grid_size * cell_size

# Set the window size
window_width = grid_width
window_height = grid_height + 70
window = pygame.display.set_mode((window_width, window_height))

# Set the window title
pygame.display.set_caption("Sudoku Land")

# Create a 2D list to store the grid values
grid = [[8, 0, 0, 0, 0, 0, 6, 0, 0], [0, 0, 7, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 3, 0, 0, 6, 0], [0, 2, 6, 0, 9, 4, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 3], [0, 0, 2, 0, 5, 0, 0, 4, 0], [0, 0, 0, 0, 0, 0, 0, 3, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

#pour reprendre la partie précedente
#x = sauvegarde_.read("sauvegarde.txt")
#grid = ast.literal_eval(x)
print(grid)



color_grid = [[WHITE] * grid_size for _ in range(grid_size)]

# Variable to store the currently selected cell position
selected_cell = None

# Variables for the timer
start_time = time.time()
paused = False
pause_time = 0

# Function to draw the grid and numbers on the screen
def draw_grid():
    window.fill(WHITE)

    # Draw the cells
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size
            pygame.draw.rect(window, color_grid[row][col], (x, y, cell_size, cell_size))
            if col % math.floor(math.sqrt(grid_size)) != 0:
                pygame.draw.line(window, COLORFUL, (x, y), (x, y + cell_size))
            if row % math.floor(math.sqrt(grid_size)) != 0:
                pygame.draw.line(window, COLORFUL, (x, y), (x + cell_size, y))
            if col % math.floor(math.sqrt(grid_size)) == 0:
                pygame.draw.line(window, BLACK, (x, y), (x, y + cell_size))
            if row % math.floor(math.sqrt(grid_size)) == 0:
                pygame.draw.line(window, BLACK, (x, y), (x + cell_size, y))
            if row == grid_size - 1:
                new = grid_size
                y1 = new * cell_size
                pygame.draw.line(window, BLACK, (x, y1), ((x + cell_size, y1)))
            if col == grid_size - 1:
                new = grid_size
                x1 = new * cell_size
                pygame.draw.line(window, BLACK, (x1, y), ((x1, y + cell_size)))
            # pygame.draw.rect(window, BLACK, (x, y, cell_size, cell_size), 1)

    # Draw the numbers
    font = pygame.font.Font(None, 36)
    for row in range(grid_size):
        for col in range(grid_size):
            value = grid[row][col]
            if value != 0:
                x = col * cell_size + cell_size // 2
                y = row * cell_size + cell_size // 2
                color = BLACK if color_grid[row][col] == WHITE else BLUE
                text = font.render(str(value), True, color)
                text_rect = text.get_rect(center=(x, y))
                window.blit(text, text_rect)

    # Draw the selected cell highlight
    if selected_cell is not None:
        row, col = selected_cell
        x = col * cell_size
        y = row * cell_size
        pygame.draw.rect(window, GREEN, (x, y, cell_size, cell_size), 3)

    # Draw the timer
    elapsed_time = int(time.time() - start_time - pause_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = f"Time: {minutes:02d}:{seconds:02d}"
    timer_font = pygame.font.Font(None, 24)
    timer_surface = timer_font.render(timer_text, True, BLACK)
    timer_rect = timer_surface.get_rect(midtop=(window_width // 2, grid_height + 10))
    window.blit(timer_surface, timer_rect)

    '''# Draw the pause button
    pause_text = "Pause" if not paused else "Resume"
    pause_font = pygame.font.Font(None, 24)
    pause_surface = pause_font.render(pause_text, True, BLACK)
    pause_rect = pause_surface.get_rect(midtop=(window_width - 70, grid_height + 10))
    window.blit(pause_surface, pause_rect)'''

    # Update the display
    pygame.display.flip()

# Function to handle events
def handle_events():
    global selected_cell, paused, pause_time, pause_rect, start_pause_time

    event = None  # Default value for the event variable

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #ici on peut récuperer les valeurs saisies pour enregistrer la grille
            sauvegarde_.sauvegarde("sauvegarde.txt", grid)
            print(grid)
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = pygame.mouse.get_pos()
                col = x // cell_size
                row = y // cell_size
                if (0 <= row < grid_size) and (0 <= col < grid_size):
                    selected_cell = (row, col)
        elif event.type == pygame.KEYDOWN:
            if selected_cell is not None:
                row, col = selected_cell
                if grid[row][col] == 0:
                    if event.unicode.isdigit() and int(event.unicode) in range(1, 10):
                        grid[row][col] = int(event.unicode)
                        color_grid[row][col] = GREY

'''# Handle the pause button click
mouse_pos = pygame.mouse.get_pos()
if pause_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
    paused = not paused
    if paused:
        start_pause_time = time.time()
    else:
        pause_time += time.time() - start_pause_time'''


def test1():
    # Main game loop
    running = True
    clock = pygame.time.Clock()

    # Create the pause button rectangle
    pause_rect = pygame.Rect(window_width - 100, grid_height + 10, 80, 30)

    while running:
        handle_events()
        if not paused:
            draw_grid()
        clock.tick(60)


    # Quit the game
    pygame.quit()
    quit()

#pour le tester (la grille)
#test1()

