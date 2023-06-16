import random
import copy
import numpy as np
import math



# Function to generate a grid for any size 4x4 9x9 16x16
def generate_sudoku(grid_size):
    # Create an empty grid

    grid = np.array([[0 for _ in range(grid_size)] for _ in range(grid_size)])


    # Fill the grid with random values
    fill_grid(grid,grid_size)

    #this part help to create an str grid so as we can change de numbre from 10 to 16 to letters from A to G
    if grid_size>9:
        grid1=np.array([['0' for _ in range(grid_size)] for _ in range(grid_size)])
        for i in range(grid_size):
            for j in range (grid_size):
                if 1<=grid[i][j]<=9:
                    grid1[i][j]=str(grid[i][j])
                elif grid[i][j]==10:
                    grid1[i][j]='A'
                elif grid[i][j]==11:
                    grid1[i][j]='B'
                elif grid[i][j]==12:
                    grid1[i][j]='C'
                elif grid[i][j]==13:
                    grid1[i][j]='D'
                elif grid[i][j]==14:
                    grid1[i][j]='E'
                elif grid[i][j]==15:
                    grid1[i][j]='F'
                else:
                    grid1[i,j]='G'
        # Return the grid completed  for a 16x16 size
        return grid1

    # Return the grid completed
    return grid

# Function to help fill the grid with random values
def fill_grid(grid, grid_size):
    square = int(grid_size ** (0.5))
    # Fill de diagonale of each under grid #Remplir la diagonale de chaque sous-grille
    for i in range(0, grid_size, square):
        fill_subgrid(grid, i, i,grid_size)

    # Fill the empty space of the grid that miss
    solve_grid(grid, grid_size)

# Function to fill the under grid of the grid
def fill_subgrid(grid, row, col, grid_size):
    square = int(grid_size ** (0.5))

    nums = list(range(1, len(grid)+1))

    # this instruction helps to choose any number of the list randomly by mixing it
    random.shuffle(nums)

    for i in range(square):
        for j in range(square):
            # the instruction pop helps to choose the value from the mixed list
            grid[row + i][col + j] = nums.pop()



# Function to solve the sudoku grid
def solve_grid(grid,grid_size):
    # here we need to know if there is an empty cell that we must fill in
    find = find_empty(grid,grid_size)
    if not find:
        return True
    else:
        row, col = find

    # if true , we try to help fixing it
    for num in range(1, grid_size+1):
        if is_valid(grid, num, row, col,grid_size):
            grid[row][col] = num

            if solve_grid(grid,grid_size):
                return True

            grid[row][col] = 0


    return False

# Function to make sure that the value input is in the right position (parameters)
def is_valid(grid, num, row, col, grid_size):
    square = int(grid_size ** (0.5))
    # Verify the row
    if num in grid[row]:
        return False

    # Verify the column
    for i in range(grid_size):
        if num == grid[i][col]:
            return False


    # Verify the subgrid
    start_row = (row // square) * square
    start_col = (col // square) * square

    for i in range(square):
        for j in range(square):
            if num == grid[start_row + i][start_col + j]:
                return False


    return True

# Function to find an empty cell of the grid
def find_empty(grid,grid_size):
    for i in range(grid_size):
        for j in range(grid_size):
            #if grid_size<10:
            if grid[i][j] == 0:
                return (i, j)
            #if grid_size>9:
                #if grid[i][j] == '0':
                    #return (i, j)

    return None

# Function  to print well the grid
def print_grid(grid,grid_size):
    racine = int(grid_size ** 0.5)
    for i in range(grid_size):
        if i % racine == 0 and i != 0:
            print('- ' * (grid_size + racine - 1))
        for j in range(grid_size):
            if j % racine == 0 and j != 0:
                print('|', end=' ')
            if grid[i][j] != 0:
                print(grid[i][j], end=' ')
            else:
                print('_', end=' ')
        print()

#the test we made to make sur all the functions work
'''# Fonction pour générer une grille de Sudoku avec un niveau de difficulté donné
grid_sol = generate_sudoku(grid_size)
peps=np.copy(grid_sol)
print_grid(grid_sol)'''

#Function to generate a sudoku compared with the difficulty
def generate_sudoku_with_difficulty(difficulty, grid_sol,grid_size):
    grid=grid_sol.copy()

    remove_count = 0
    if grid_size>4:
        if difficulty == "easy":
            remove_count = int(grid_size ** 2 * 0.35) # here is 35% of the grid is removed
        elif difficulty == "medium":
            remove_count = int(grid_size ** 2 * 0.45)# here is 45% of the grid is removed
        elif difficulty == "hard":
            remove_count = int(grid_size ** 2 * 0.65)# here is 65% of the grid is removed
        elif difficulty == "diabolical":
            remove_count = int(grid_size ** 2 * 0.78)# here is 78% of the grid is removed
    else :
        if difficulty == "easy":
            remove_count = 3
        elif difficulty == "medium":
            remove_count = 4
        elif difficulty == "hard":
            remove_count = 5
        elif difficulty == "diabolical":
            remove_count = 6


    #part to remove the cell from the solution
    while remove_count > 0:
        row = random.randint(0, grid_size-1)
        col = random.randint(0, grid_size-1)
        if grid_size < 10:
            if grid[row][col] != 0:
                grid[row][col] = 0
                remove_count -= 1
        if grid_size > 9:
            if grid[row][col] != '0':
                grid[row][col] = '0'
                remove_count -= 1

    print(grid)
    return grid


def test1(difficulty, grid_size):
    grid_sol = generate_sudoku(grid_size)
    peps = np.copy(grid_sol) # the most important part so as we can compare with what the user input in our game
    grid = generate_sudoku_with_difficulty(difficulty,grid_sol,grid_size)

    return grid,peps

#grid_size=16
#grid1,sol1=test1('easy',16)
#print_grid(grid1,grid_size)
#print_grid(sol1,grid_size)
