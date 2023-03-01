import tkinter as tk

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = False

class GridCell(tk.Canvas):
    def __init__(self, master=None, cell=None, **kwargs):
        super().__init__(master, **kwargs)
        self.cell = cell
        self.bind("<Button-1>", self.toggle_state)
        self.draw()

    def toggle_state(self, event):
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

root = tk.Tk()
cells = createGrid(10, 10)
grid = Grid(root, rows=10, cols=10)
grid.pack()

start_button = tk.Button(root, text="Start", command=startGame)
start_button.pack()

root.mainloop()
