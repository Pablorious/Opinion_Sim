import pygame as pg
from pygame import Rect
from random import randint, choice
from math import gcd
from color import Color

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
SCREEN_UNIT = int(gcd(SCREEN_WIDTH,SCREEN_HEIGHT))
TILE_SIZE = 4 * SCREEN_UNIT
GRID_WIDTH = int( SCREEN_WIDTH / TILE_SIZE )
GRID_HEIGHT = int( SCREEN_HEIGHT / TILE_SIZE )
RANGE = 3

grid = [[randint(0,RANGE) for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

EQUAL_LIGHTNESS_COLORS = Color.get_colors_by_lightness(56,0.1)

COLOR_SCHEME = { i: choice(EQUAL_LIGHTNESS_COLORS) for i in range(0,5)}

def get_surround_indices(grid, x, y):
    cols = GRID_WIDTH
    rows = GRID_HEIGHT

    neighbors = []

    if x > 0: 
        neighbors.append([x-1,y])
        if y > 0: neighbors.append([x-1,y-1])
        if y < rows - 1: neighbors.append([x-1,y+1])

    if x < cols - 1: 
        neighbors.append([x+1,y])
        if y > 0:
            neighbors.append([x+1,y-1])
        if y < rows - 1: neighbors.append([x+1,y+1])

        if y > 0: neighbors.append([x,y-1])
        if y < rows - 1: neighbors.append([x,y+1])

    return neighbors


NEIGHBORS = { (x,y) : get_surround_indices(grid,x,y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)}

def draw_tile(screen,color,x,y):
    pg.draw.rect(screen,color,Rect(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE))

def redraw_grid(screen, grid, indices):
    for (x,y) in indices:
        tile = grid[x][y]
        color = COLOR_SCHEME[tile]
        draw_tile(screen,color,x,y)

def draw_grid(screen,grid):
    for x,tiles in enumerate(grid):
        for y,tile in enumerate(tiles):
            color = (96,0,255)
            if tile == 1: color = (94,48,255)
            draw_tile(screen,color,x,y) 
  
def update(grid):
    new_grid = []
    indices_of_updated_tiles = []
    for x,tiles in enumerate(grid):
        new_tiles = []
        for y,_ in enumerate(tiles):
            indices = NEIGHBORS[(x,y)]
            neighbors = []
            for [x,y] in indices:
                neighbors.append(grid[x][y])
            new_tile = choice(neighbors)
            if grid[x][y] != new_tile:
                indices_of_updated_tiles.append((x,y))
            new_tiles.append(new_tile)
        new_grid.append(new_tiles)
    return [new_grid, indices_of_updated_tiles]

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pg.FULLSCREEN)
running = True
pg.display.set_caption("Opinion Change Modeling")
 
draw_grid(screen,grid)
while(running):
    pg.display.update()
    
    grid,indices_of_updated_tiles = update(grid)
    redraw_grid(screen,grid, indices_of_updated_tiles)

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.QUIT:
            running = False
   
pg.quit()
