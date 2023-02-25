import numpy as np
import pygame
GRID_SIZE = (50, 50)
CELL_SIZE = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
pygame.init()
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode((GRID_SIZE[0] * CELL_SIZE, GRID_SIZE[1] * CELL_SIZE))
clock = pygame.time.Clock()
grid = np.zeros(GRID_SIZE)
grid[5][5] = 1
grid[5][6] = 1
grid[5][7] = 1
def update_grid(grid):
    new_grid = np.copy(grid)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbors = grid[max(0, i-1):min(i+2, grid.shape[0]), 
                             max(0, j-1):min(j+2, grid.shape[1])]
            count = np.sum(neighbors) - grid[i][j]
            if count == 3:
                new_grid[i][j] = 1
            elif count != 2:
                new_grid[i][j] = 0
    return new_grid
def handle_input(grid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            i = x // CELL_SIZE
            j = y // CELL_SIZE
            if event.button == 1:  # Left button sets cell to alive
                grid[i][j] = 1
            elif event.button == 3:  # Right button sets cell to dead
                grid[i][j] = 0
while True:
    handle_input(grid)
    grid = update_grid(grid)
    screen.fill(BLACK)
    for i in range(GRID_SIZE[0]):
        for j in range(GRID_SIZE[1]):
            if grid[i][j] == 1:
                pygame.draw.rect(screen, WHITE, (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    x, y = pygame.mouse.get_pos()
    i = x // CELL_SIZE
    j = y // CELL_SIZE
    pygame.draw.rect(screen, GREEN, (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
