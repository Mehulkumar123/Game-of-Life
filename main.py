import tkinter as tk
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
BG_COLOR = 'white'
CELL_COLOR = 'black'
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 0
        self.rect = None
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
def pauseGame():
    global begin_id
    canvas.after_cancel(begin_id)
def exitGame():
    root.destroy()
def reset():
    global cells, begin_id
    canvas.after_cancel(begin_id)
    cells = [[Cell(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            canvas.itemconfig(cells[x][y].rect, fill=BG_COLOR)
            cells[x][y].state = 0
root = tk.Tk()
root.title('Conway\'s Game of Life')
canvas = tk.Canvas(root, width=GRID_WIDTH*CELL_SIZE, height=GRID_HEIGHT*CELL_SIZE)
canvas.pack()
createGrid(canvas)
canvas.bind('<Button-1>', changeColor)
start_button = tk.Button(root, text='Start', command=startGame)
start_button.pack(side='left')
pause_button = tk.Button(root, text='Pause', command=pauseGame)
pause_button.pack(side='left')
reset_button = tk.Button(root, text='Reset', command=reset)
reset_button.pack(side='left')
exit_button = tk.Button(root, text='Exit', command=exitGame)
exit_button.pack(side='left')
begin_id = None
root.mainloop()
