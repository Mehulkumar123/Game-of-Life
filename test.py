import tkinter as tk

is_paused = False

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = False
        self.next_state = False

class GridCell(tk.Canvas):
    def __init__(self, master=None, cell=None, **kwargs):
        super().__init__(master, **kwargs)
        self.cell = cell
        self.bind("<Button-1>", self.changeColour)
        self.draw()

    def changeColour(self, event):
        self.cell.state = not self.cell.state
        self.draw()

    def draw(self):
        if self.cell.state:
            self.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), fill="black")
        else:
            self.delete("all")

class Grid(tk.Frame):
    def __init__(self, master=None, rows=10, cols=10, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(i, j) for j in range(cols)] for i in range(rows)]
        self.grid_cells = []
        for row in range(rows):
            row_cells = []
            for col in range(cols):
                cell = GridCell(self, cell=self.cells[row][col], width=20, height=20, bd=1, relief="raised")
                cell.grid(row=row, column=col)
                row_cells.append(cell)
            self.grid_cells.append(row_cells)

    def changeCellState(self):
        for row in range(self.rows):
            for col in range(self.cols):
                live_neighbors = 0
                for i in range(row-1, row+2):
                    for j in range(col-1, col+2):
                        if i == row and j == col:
                            continue
                        if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
                            continue
                        if self.cells[i][j].state:
                            live_neighbors += 1
                if self.cells[row][col].state:
                    if live_neighbors in [2, 3]:
                        self.cells[row][col].next_state = True
                    else:
                        self.cells[row][col].next_state = False
                else:
                    if live_neighbors == 3:
                        self.cells[row][col].next_state = True
                    else:
                        self.cells[row][col].next_state = False

        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].state = self.cells[row][col].next_state

        self.updateGrid()

    def updateGrid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid_cells[row][col].cell = self.cells[row][col]
                self.grid_cells[row][col].draw()

def createGrid(rows, cols):
    cells = [[Cell(i, j) for j in range(cols)] for i in range(rows)]
    return cells

def startGame():
    global is_paused
    if not is_paused:
        grid.changeCellState()
        root.after(1000, startGame)

def pauseGame():
    global is_paused
    is_paused = True

def exitGame():
    root.destroy()

def reset():
    global is_paused
    is_paused = True
    for row in range(grid.rows):
        for col in range(grid.cols):
            grid.cells[row][col].state = False
    grid.updateGrid()

root = tk.Tk()
cells = createGrid(10, 10)
grid = Grid(root, rows=20, cols=20)
grid.pack()

start_button = tk.Button(root, text="Start", command=startGame)
start_button.pack()

pause_button = tk.Button(root, text="Pause", command=pauseGame)
pause_button.pack()

reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.pack()

exit_button = tk.Button(root, text="Exit", command=exitGame)
exit_button.pack()

root.mainloop()
