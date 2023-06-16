import pygame
import time
import math
import numpy as np
import Levels3
from pygame.locals import *
import sauvegarde_
import os
import button_class
import ast

# Define some principal colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
COLORFUL = (100, 191, 255)
BLUE2 = (212, 231, 255)
BLUE3 = (15, 5, 107)

# Initialize Pygame
pygame.init()


def set_dimensions_grid(grid_size):
    # Set the dimensions of the grid and cells
    if grid_size > 9:
        cell_size = 26
    else:
        cell_size = 50
    grid_width = grid_height = grid_size * cell_size
    return cell_size


# Set the window title
pygame.display.set_caption("Sudoku Land")


# Variable to store the currently selected cell position and the state of the grid
selected_cell = None
completed = False


#Function to check if the grid is completed or no
def check_grid_completed(grid, sol, grid_size):
    for row in range(grid_size):
        for col in range(grid_size):
            if grid_size < 10:
                if grid[row][col] == 0:
                    return False
            else:
                if grid[row][col] == '0':
                    return False
    return True


# fonction to show the next window according to which button you clicked on
def enter_button(menu_state, clicked, text):
    menu_state = text
    pygame.display.set_caption(menu_state)
    clicked = True
    pygame.display.update()
    return menu_state, clicked

# function to draw the button on the screen (it is used for the main game button when we are in the game state)
def draw_button(window, clicked, menu_state):
    menu_image = pygame.image.load(os.path.join('images', 'main_menu.PNG'))
    menu_button = button_class.Button(480, 15, 0.99, menu_image)
    if menu_button.draw(window) and not clicked:
        menu_state, clicked = enter_button(menu_state, clicked, "Main Sudoku Land")
    #print(menu_state)
    return menu_state, clicked


# Function to draw the grid and numbers on the screen
def draw_grid(grid, sol, grid_size, window, cell_size, color_grid, window_width, grid_height, strikes, start_time, pause_time):
    # the start position to draw the grid to make it fit well in the interface
    if grid_size == 4:
        start_x = 40
        start_y = 200
    elif grid_size == 9:
        start_x = 10
        start_y = 85
    else:
        start_x = 10
        start_y = 100

    # Draw the cells
    for row in range(grid_size):
        for col in range(grid_size):
            x = start_x + col * cell_size
            y = start_y + row * cell_size
            pygame.draw.rect(window, color_grid[row][col], (x, y, cell_size, cell_size))
            #here it draw the line in function of the modulo (color)
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
                y1 = start_y + new * cell_size
                pygame.draw.line(window, BLACK, (x, y1), ((x + cell_size, y1)))
            if col == grid_size - 1:
                new = grid_size
                x1 = start_x + new * cell_size
                pygame.draw.line(window, BLACK, (x1, y), ((x1, y + cell_size)))

    # Draw the numbers with different font in relation to the size of the grid
    if grid_size < 10:
        font = pygame.font.Font(None, 36)
    else:
        font = pygame.font.Font(None, 25)

    for row in range(grid_size):
        for col in range(grid_size):
            value = grid[row][col]
            if grid_size < 10:
                if value != 0:
                    # some calculus to make sure the number is centered in the cell
                    x = start_x + col * cell_size + cell_size // 2
                    y = start_y + row * cell_size + cell_size // 2
                    color = BLACK if color_grid[row][col] == WHITE else BLUE
                    text = font.render(str(value), True, color)
                    text_rect = text.get_rect(center=(x, y))
                    window.blit(text, text_rect)
            else:
                if value != '0':
                    x = start_x + col * cell_size + cell_size // 2
                    y = start_y + row * cell_size + cell_size // 2
                    color = BLACK if color_grid[row][col] == WHITE else BLUE
                    text = font.render(str(value), True, color)
                    text_rect = text.get_rect(center=(x, y))
                    window.blit(text, text_rect)

    # Draw the selected cell highlight
    if selected_cell is not None:
        row, col = selected_cell
        x = start_x + col * cell_size
        y = start_y + row * cell_size
        pygame.draw.rect(window, GREEN, (x, y, cell_size, cell_size), 3)

    #draw a white rectangle so as we can display the strikes and the timer
    pygame.draw.rect(window, WHITE, ((480, 239), (150, 239)))

    # Draw the strikes
    strike_font = pygame.font.Font(None, 30)
    strike_text = "Erreur: {}/5".format(strikes)
    strike_surface = strike_font.render(strike_text, True, BLUE3)
    strike_rect = strike_surface.get_rect(center=(550, 350))
    window.blit(strike_surface, strike_rect)

    # Draw the timer
    elapsed_time = int(time.time() - start_time) + pause_time # the pause time help to restart the game where we call off to play later
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = f"Timer: {minutes:02d}:{seconds:02d}"
    timer_font = pygame.font.Font(None, 30)
    timer_surface = timer_font.render(timer_text, True, BLUE3)
    timer_rect = timer_surface.get_rect(center=(550, 300))
    window.blit(timer_surface, timer_rect)


    # Update the display
    pygame.display.flip()

    # Update the display
    pygame.display.flip()

    return elapsed_time

#Function to choose the level and the grid
def choisir_grille(niveau, grid_size):
    grid, sol = Levels3.test1(niveau, grid_size)
    return grid, sol


# Function to handle events
def handle_events(grid, sol, grid_size, cell_size, color_grid, grid_width, grid_height, clicked,strikes):
    global selected_cell, completed

    # to define the place where the user can click (on the button) to enter the menu
    clickable_area1 = pygame.Rect((480, 18), (143, 40))
    rect_surface1 = pygame.Surface(clickable_area1.size)
    rect_surface1.set_alpha(0)

    # to define the place where we can click (so the button) to solve the sudoku
    clickable_area2 = pygame.Rect((483, 503), (136, 20))
    rect_surface2 = pygame.Surface(clickable_area2.size)
    rect_surface2.set_alpha(0)

    event = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # 1= clique gauche
                if clickable_area1.collidepoint(event.pos) :
                    clicked = False
                    print("yes")
                if clickable_area2.collidepoint(event.pos):
                    for i in range(grid_size):
                        for j in range(grid_size):
                            if grid_size<10:
                                if grid[i][j] == 0:
                                    color_grid[i][j] = BLUE2
                                    grid[i][j] = sol[i][j]
                            else:
                                if grid[i][j] == '0':
                                    color_grid[i][j] = BLUE2
                                    grid[i][j] = sol[i][j]

        elif event.type == pygame.MOUSEBUTTONDOWN:
           #here to draw the right selected cell with the beginning of the grid
            if event.button == 1:  # Left mouse button
                x, y = pygame.mouse.get_pos()
                if grid_size == 4:
                    start_x = 40
                    start_y = 200
                elif grid_size == 9:
                    start_x = 10
                    start_y = 85
                else:
                    start_x = 10
                    start_y = 100
                if (
                        start_x <= x < start_x + grid_width
                        and start_y <= y < start_y + grid_height
                ):
                    col = (x - start_x) // cell_size
                    row = (y - start_y) // cell_size
                    if (0 <= row < grid_size) and (0 <= col < grid_size):
                        selected_cell = (row, col)
        # here the event to input our values
        elif event.type == pygame.KEYDOWN:
            if selected_cell is not None:
                row, col = selected_cell
                if grid_size<10:
                    if grid[row][col] == 0:
                        if event.unicode.isdigit() and int(event.unicode) in range(1, grid_size + 1):
                            value = int(event.unicode)
                            if value == sol[row][col]:
                                grid[row][col] = value
                                color_grid[row][col] = GREY
                                Levels3.print_grid(grid, grid_size)
                            #Verify if the game is over or not
                                if check_grid_completed(grid, sol, grid_size):
                                    completed = True
                            else:
                                strikes += 1
                else :
                    if grid[row][col] == '0':
                        if event.unicode in '123456789ABCDEFG':
                             value = str(event.unicode)
                             if value==sol[row][col]:
                                grid[row][col]= value
                                color_grid[row][col] = GREY
                                Levels3.print_grid(grid, grid_size)
                                if check_grid_completed(grid, sol, grid_size):
                                    completed = True
                             else:
                                strikes += 1

    return clicked,strikes


# Function to run the game
def test(grid_size, window, window_width, grid_height, menu_state, clicked):
    # Main game loop
    running = True
    color_grid = [[WHITE] * grid_size for _ in range(grid_size)]
    clock = pygame.time.Clock()
    level = sauvegarde_.read("niveau.txt")
    cell_size = set_dimensions_grid(grid_size)
    # Variables for the timer
    start_time = time.time()
    paused = False
    pause_time = 0

    # Variable to store the strikes count
    strikes = 0

    if menu_state in ("easy", "medium", "hard", "diabolical"):
        grid, sol = choisir_grille(level, grid_size)
        #sauvegarde_.sauvegarde("sauvegarde.txt", grid)
    elif menu_state == "resume":
        # to resume the previous game stored in a text file
        x = sauvegarde_.read("sauvegarde.txt")
        y= sauvegarde_.read("erreur.txt")
        z= sauvegarde_.read("timer.txt")
        # to convert the representation of a string list into a list
        a = str(x).replace(' ',', ')
        sol = ast.literal_eval(a)
        # we check that everything is good
        print(type(sol))


        grid = np.copy(sol)
        strikes =int(y)
        pause_time= int(z)
        Levels3.solve_grid(sol, grid_size)
        Levels3.print_grid(grid, grid_size)

    while clicked == False:
        menu_state, clicked = draw_button(window, clicked, menu_state)
        clicked,strikes = handle_events(grid, sol, grid_size, cell_size, color_grid, window_width, grid_height, clicked,strikes)
        ok=draw_grid(grid, sol, grid_size, window, cell_size, color_grid, window_width, grid_height,strikes,start_time,pause_time)

        sauvegarde_.sauvegarde("sauvegarde.txt", grid)
        sauvegarde_.sauvegarde("erreur.txt",strikes)
        sauvegarde_.sauvegarde('timer.txt',ok)
        clock.tick(60)
        if check_grid_completed(grid, sol, grid_size) == True:
            time.sleep(3)
            menu_state = "victoire"
            return menu_state, clicked
        if strikes == 5:
            menu_state = "defaite"
            return menu_state, clicked


    return menu_state, clicked

#window = pygame.display.set_mode((662, 555))
#test(9,window , 644, 460)
