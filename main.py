import tkinter as tk
from tkinter import ttk

# constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
BG_COLOR = 'white'
CELL_COLOR = 'black'

# Cell class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 0
        self.rect = None

# create the grid
def createGrid(canvas):
    global cells
    cells = [[Cell(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = canvas.create_rectangle(
                x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE,
                fill=BG_COLOR, outline='gray'
            )
            cells[x][y].rect = rect

# change the color of a cell when clicked
def changeColor(event):
    global cells
    x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
    cell = cells[x][y]
    if cell.state == 0:
        canvas.itemconfig(cell.rect, fill=CELL_COLOR)
        cell.state = 1
    else:
        canvas.itemconfig(cell.rect, fill=BG_COLOR)
        cell.state = 0

# change the state of a cell based on its neighbors
def changeCellState(cell):
    global cells
    x, y = cell.x, cell.y
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if x+i < 0 or x+i >= GRID_WIDTH or y+j < 0 or y+j >= GRID_HEIGHT:
                continue
            neighbors.append(cells[x+i][y+j])
    live_neighbors = sum(n.state for n in neighbors)
    if cell.state == 1 and (live_neighbors < 2 or live_neighbors > 3):
        cell.next_state = 0
    elif cell.state == 0 and live_neighbors == 3:
        cell.next_state = 1
    else:
        cell.next_state = cell.state

# advance the game by one iteration
def startGame():
    global cells, begin_id
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            changeCellState(cells[x][y])
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell = cells[x][y]
            cell.state = cell.next_state
            if cell.state == 0:
                canvas.itemconfig(cell.rect, fill=BG_COLOR)
            else:
                canvas.itemconfig(cell.rect, fill=CELL_COLOR)
    begin_id = canvas.after(100, startGame)

# pause the game
def pauseGame():
    global begin_id
    canvas.after_cancel(begin_id)

# exit the game
def exitGame():
    root.destroy()

# reset the game
def reset():
    global cells, begin_id
    canvas.after_cancel(begin_id)
    cells = [[Cell(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            canvas.itemconfig(cells[x][y].rect, fill=BG_COLOR)

# apply a pattern to the grid
def applyPattern(pattern):
    reset()
    x_offset = (GRID_WIDTH - pattern.width) // 2
    y_offset = (GRID_HEIGHT - pattern.height) // 2
    for x in range(pattern.width):
        for y in range(pattern.height):
            cell = cells[x+x_offset][y+y_offset]
            if pattern.grid[y][x] == 1:
                cell.state = 1
                canvas.itemconfig(cell.rect, fill=CELL_COLOR)
            else:
                cell.state = 0
                canvas.itemconfig(cell.rect, fill=BG_COLOR)

# patterns = [
# {'name': 'Glider', 'pattern': Pattern([[0, 1, 0], [0, 0, 1], [1, 1, 1]])},
# {'name': 'Blinker', 'pattern': Pattern([[0, 1, 0], [0, 1, 0], [0, 1, 0]])},
# {'name': 'Pulsar', 'pattern': Pattern([[0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],[1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],[1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],[1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],[0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],[0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],[1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],[1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],[1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],[0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],])},]

def resetGame():
    global cells, begin_id
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell = cells[x][y]
            cell.state = 0
            cell.next_state = 0
            canvas.itemconfig(cell.rect, fill=BG_COLOR)
    canvas.after_cancel(begin_id)

# create the GUI
root = tk.Tk()
root.title("Game of Life")

# create the canvas
canvas = tk.Canvas(root, width=GRID_WIDTH*CELL_SIZE, height=GRID_HEIGHT*CELL_SIZE, bg=BG_COLOR)
canvas.pack()

# create the grid and allow cell clicks
createGrid(canvas)
canvas.bind("<Button-1>", changeColor)

# create the buttons
button_frame = ttk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)
start_button = ttk.Button(button_frame, text="Start", command=startGame)
start_button.pack(side=tk.LEFT, padx=5)
pause_button = ttk.Button(button_frame, text="Pause", command=pauseGame)
pause_button.pack(side=tk.LEFT, padx=5)
reset_button = ttk.Button(button_frame, text="Reset", command=resetGame)
reset_button.pack(side=tk.LEFT, padx=5)
exit_button = ttk.Button(button_frame, text="Exit", command=exitGame)
exit_button.pack(side=tk.LEFT, padx=5)

# run the GUI
root.mainloop()
