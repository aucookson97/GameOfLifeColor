from pygame import *
import sys
from random import random, choice

STATUS_HEIGHT = 50

PRIMARY = ([255, 0, 0], [0, 255, 0], [0, 0, 255])
NOCELL = [255, 255, 255]
BLACK = [0, 0, 0]

GRID_WIDTH = 40 # Number of Cell Columns
GRID_HEIGHT = 40 # Number of Cell Rows

CELL_SIZE = 20 # Cell Dimensions in Pixels

generation_speed_select = 3 
GENERATION_SPEED = (10, 100, 500, 1000, 2000, 5000, 10000) # Generation Length in Milliseconds

color = True

# Initialize Cells to None
cells = [[NOCELL for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

def run():
    global generation_speed_select, color
    
    generation_number = 0 # Keeps Track of Current Generation
    last_generation = time.get_ticks()
    running = True
    while running:
        for i in event.get():
            if (i.type == QUIT):
                running = False
            elif (i.type == KEYDOWN):
                print (i.key)
                if (i.key == 273): # UP
                    generation_speed_select = min(generation_speed_select + 1, len(GENERATION_SPEED) - 1)
                    print("Generation Speed Set To: {}ms".format(GENERATION_SPEED[generation_speed_select]))
                if (i.key == 274): # DOWN
                    generation_speed_select= max(generation_speed_select - 1, 0)
                    print("Generation Speed Set To: {}ms".format(GENERATION_SPEED[generation_speed_select]))
                if (i.key == 32): # SPACE
                    print ("Randomizing Cells...")
                    generation_number = 0
                    randomizeCells(color)
                if (i.key == 99): # c
                    print ("Toggling Color...")
                    color = not color
                    randomizeCells(color)

                if (i.key == 110): # n
                    print ("Adding Noise...")
                    addNoise()
                    

        # Wait for Next Generation
        if (time.get_ticks() - last_generation >= GENERATION_SPEED[generation_speed_select]): 
            print("Generation: {}".format(generation_number))

            # Graphics
            screen.fill(NOCELL)
            drawGrid()
            drawCells()
            display.update()

            evolve()
            
            generation_number += 1
            last_generation = time.get_ticks()
    quit()
    sys.exit()

# Calculate Cell States for Next Generation
def evolve():
    global cells

    # Create Temporary Copy to Edit
    new_cells = shallow_copy(cells)
    
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors, color_ave = countNeighbors(x, y)

            # Cell is Currently Alive
            if (cells[y][x] != NOCELL):
                if (neighbors < 2 or neighbors > 3):
                    new_cells[y][x] = NOCELL
            # Cell is Currently Dead
            elif (neighbors == 3):
                new_cells[y][x] = color_ave

    cells = shallow_copy(new_cells)
    
# Count Number of Neighbors of a Cell and the Average Neighbor Color
def countNeighbors(x, y):
    neighbors = 0

    color_sum = [0, 0, 0]

    if (x-1 >= 0 and y-1 >= 0 and cells[y-1][x-1] != NOCELL):
        neighbors += 1
        color_sum[0] += cells[y-1][x-1][0]
        color_sum[1] += cells[y-1][x-1][1]
        color_sum[2] += cells[y-1][x-1][2]
    if (x-1 >= 0 and cells[y][x-1] != NOCELL):
        neighbors += 1
        color_sum[0] += cells[y][x-1][0]
        color_sum[1] += cells[y][x-1][1]
        color_sum[2] += cells[y][x-1][2]
    if (y-1 >= 0 and cells[y-1][x] != NOCELL):
        neighbors += 1
        color_sum[0] += cells[y-1][x][0]
        color_sum[1] += cells[y-1][x][1]
        color_sum[2] += cells[y-1][x][2]
    if (x-1 >= 0 and y+1 < GRID_HEIGHT and cells[y+1][x-1] != NOCELL):
        neighbors += 1
        color_sum[0] += cells[y+1][x-1][0]
        color_sum[1] += cells[y+1][x-1][1]
        color_sum[2] += cells[y+1][x-1][2]
    if (y-1 >= 0 and x+1 < GRID_WIDTH and cells[y-1][x+1] != NOCELL):
        neighbors += 1
        color_sum[0] += cells[y-1][x+1][0]
        color_sum[1] += cells[y-1][x+1][1]
        color_sum[2] += cells[y-1][x+1][2]
    if (x+1 < GRID_WIDTH and cells[y][x+1] != NOCELL):
        neighbors += 1
        color_sum[0] += cells[y][x+1][0]
        color_sum[1] += cells[y][x+1][1]
        color_sum[2] += cells[y][x+1][2]
    if (y+1 < GRID_HEIGHT and cells[y+1][x] != NOCELL):
        neighbors += 1
        color_sum[0] += cells[y+1][x][0]
        color_sum[1] += cells[y+1][x][1]
        color_sum[2] += cells[y+1][x][2]
    if (x+1 < GRID_WIDTH and y+1 < GRID_HEIGHT and cells[y+1][x+1] != NOCELL):
        neighbors += 1
        color_sum[0] += cells[y+1][x+1][0]
        color_sum[1] += cells[y+1][x+1][1]
        color_sum[2] += cells[y+1][x+1][2]
    if (neighbors != 0):
        color_ave = [int(color_sum[0] / neighbors), int(color_sum[1] / neighbors), int(color_sum[2] / neighbors)]
    else:
        color_ave = NOCELL
    return neighbors, color_ave

def drawCells():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = Rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1)
            draw.rect(screen, cells[y][x], rect, 0)

def drawGrid():
    for x in range(GRID_WIDTH):
        draw.line(screen, BLACK, (int(x * CELL_SIZE), 0), (int(x * CELL_SIZE), screen_size[1]), 1)

    for y in range(GRID_HEIGHT):
        draw.line(screen, BLACK, (0, int(y * CELL_SIZE)), (screen_size[0], int(y * CELL_SIZE)), 1)

def addNoise():
    global cells
    noise_chance = .05

    for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if (random() < noise_chance):
                    if (color):
                        cells[y][x] = choice(PRIMARY)
                    else:
                        cells[y][x] = [0, 0, 0]

def randomizeCells(isColored):
    global cells

    cells = [[NOCELL for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

    cell_chance = .3 # % Chance a Cell Will be Filled
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (random() < cell_chance):
                if (isColored):
                    cells[y][x] = choice(PRIMARY)
                else:
                    cells[y][x] = [0, 0, 0]

def printCells():
    for y in range(GRID_HEIGHT):
        s = ""
        for x in range(GRID_WIDTH):
            s += str(cells[y][x]) + ", "
        print(s)

def shallow_copy(arr2d):
    new_arr2d = [[arr2d[y][x].copy() for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
    return new_arr2d

    
if __name__ == "__main__":
    global screen, screen_size

    init()

    # Initialize Display Window
    screen_size = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE + STATUS_HEIGHT)
    screen = display.set_mode(screen_size)
    display.set_caption("Conway's Game of Life - Color")

    randomizeCells(color)

    run()
