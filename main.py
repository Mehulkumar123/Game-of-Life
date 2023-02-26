import tkinter as tk
import random

# Define constants
CELL_SIZE = 20
ROWS = 25
COLS = 25

# Create the Cell class
class Cell:
    def __init__(self, row, col, state=0):
        self.row = row
        self.col = col
        self.state = state
        self.rect_id = None

    def draw(self, canvas):
        x0 = self.col * CELL_SIZE
        y0 = self.row * CELL_SIZE
        x1 = (self.col + 1) * CELL_SIZE
        y1 = (self.row + 1) * CELL_SIZE
        if self.state == 1:
            fill = "black"
        else:
            fill = "white"
        self.rect_id = canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="gray")

    def toggle(self, canvas):
        self.state = 1 - self.state
        canvas.itemconfigure(self.rect_id, fill="black" if self.state == 1 else "white")

# Initialize the grid of cells
grid = [[Cell(i, j) for j in range(COLS)] for i in range(ROWS)]

# Create the GUI
root = tk.Tk()
root.title("Game of Life")

canvas = tk.Canvas(root, width=CELL_SIZE*COLS, height=CELL_SIZE*ROWS)
canvas.pack()

def create_grid():
    for row in grid:
        for cell in row:
            cell.draw(canvas)

def change_colour(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    cell = grid[y][x]
    cell.toggle(canvas)

canvas.bind("<Button-1>", change_colour)

def get_neighbours(row, col):
    neighbours = []
    for i in range(max(row-1, 0), min(row+2, ROWS)):
        for j in range(max(col-1, 0), min(col+2, COLS)):
            if (i, j) != (row, col):
                neighbours.append(grid[i][j])
    return neighbours

def change_cell_state(cell):
    neighbours = get_neighbours(cell.row, cell.col)
    live_count = sum(neighbour.state for neighbour in neighbours)
    if cell.state == 1:
        if live_count < 2 or live_count > 3:
            return 0
    else:
        if live_count == 3:
            return 1
    return cell.state

def start_game():
    global begin_id
    new_grid = [[Cell(i, j, change_cell_state(cell)) for j, cell in enumerate(row)] for i, row in enumerate(grid)]
    grid[:] = new_grid
    for row in grid:
        for cell in row:
            cell.draw(canvas)
    begin_id = root.after(500, start_game)

def pause_game():
    root.after_cancel(begin_id)

def exit_game():
    root.destroy()

def reset():
    global begin_id
    if begin_id:
        root.after_cancel(begin_id)
    grid[:] = [[Cell(i, j, random.randint(0, 1)) for j in range(COLS)] for i in range(ROWS)]
    for row in grid:
        for cell in row:
            cell.draw(canvas)


begin_id = None

reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.pack(side=tk.LEFT)

start_button = tk.Button(root, text="Start", command=start_game)
start_button.pack(side=tk.LEFT)

pause_button = tk.Button(root, text="Pause", command=pause_game)
pause_button.pack(side=tk.LEFT)

exit_button = tk.Button(root, text="Exit", command=exit_game)
exit_button.pack(side=tk.LEFT)

create_grid()
reset()

root.mainloop()
