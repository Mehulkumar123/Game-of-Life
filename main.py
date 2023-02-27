import tkinter as tk
from tkinter import ttk
import random

# constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
BG_COLOR = 'white'
CELL_COLOR = 'black'
CELL_SIZEGRID_WIDTH = GRID_WIDTH * CELL_SIZE

# Cell class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 0
        self.next_state = 0  # add next_state attribute to keep track of the next state
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
            canvas.tag_bind(rect, '<Button-1>', changeColor)
            canvas.tag_bind(rect, '<B1-Motion>', changeColor)


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

def addPattern(pattern):
    global cells
    x_offset, y_offset = (GRID_WIDTH // 2) - (len(pattern[0]) // 2), (GRID_HEIGHT // 2) - (len(pattern) // 2)
    for y in range(len(pattern)):
        for x in range(len(pattern[y])):
            cells[x+x_offset][y+y_offset].state = pattern[y][x]
            if pattern[y][x] == 0:
                canvas.itemconfig(cells[x+x_offset][y+y_offset].rect, fill=BG_COLOR)
            else:
                canvas.itemconfig(cells[x+x_offset][y+y_offset].rect, fill=CELL_COLOR)
# clear the canvas
def clearCanvas():
    global cells, begin_id
    canvas.after_cancel(begin_id)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cells[x][y].state = 0
            canvas.itemconfig(cells[x][y].rect, fill=BG_COLOR)

# randomly fill the grid with cells
def randomFill():
    global cells
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell = cells[x][y]
            cell.state = random.choice([0, 1])
            if cell.state == 0:
                canvas.itemconfig(cell.rect, fill=BG_COLOR)
            else:
                canvas.itemconfig(cell.rect, fill=CELL_COLOR)

# create the UI
root = tk.Tk()
root.title('Conway\'s Game of Life')

canvas = tk.Canvas(root, width=CELL_SIZEGRID_WIDTH, height=GRID_HEIGHT*CELL_SIZE)
canvas.pack()

createGrid(canvas)

# add buttons
frame = ttk.Frame(root)
frame.pack(side=tk.BOTTOM)

start_button = ttk.Button(frame, text='Start', command=startGame)
start_button.pack(side=tk.LEFT, padx=5)

pause_button = ttk.Button(frame, text='Pause', command=pauseGame)
pause_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(frame, text='Clear', command=clearCanvas)
clear_button.pack(side=tk.LEFT, padx=5)

random_button = ttk.Button(frame, text='Random Fill', command=randomFill)
random_button.pack(side=tk.LEFT, padx=5)

exit_button = ttk.Button(frame, text='Exit', command=exitGame)
exit_button.pack(side=tk.LEFT, padx=5)

glider_pattern = [
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1]
]
ttk.Button(root, text='Glider', command=lambda: addPattern(glider_pattern)).pack(side=tk.LEFT)

lwss_pattern = [
    [0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0]
]
ttk.Button(root, text='Lwss', command=lambda: addPattern(lwss_pattern)).pack(side=tk.LEFT)

beacon_pattern = [
    [1, 1, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, 1, 1]
]
ttk.Button(root, text='Beacon', command=lambda: addPattern(beacon_pattern)).pack(side=tk.LEFT)

toad_pattern = [
    [0, 0, 0, 0],
    [0, 1, 1, 1],
    [1, 1, 1, 0],
    [0, 0, 0, 0]
]
ttk.Button(root, text='Toad', command=lambda: addPattern(toad_pattern)).pack(side=tk.LEFT)

blinker = [
    [0, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
]
ttk.Button(root, text='Blinker', command=lambda: addPattern(blinker)).pack(side=tk.LEFT)

pulsar_pattern = [
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,1,1,1,0,0],
]
ttk.Button(root, text='Pulsar', command=lambda: addPattern(pulsar_pattern)).pack(side=tk.LEFT)

# run the tkinter event loop
root.mainloop()
