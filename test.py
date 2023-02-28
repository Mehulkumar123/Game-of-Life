import tkinter as tk

class CellGrid:
    def __init__(self, master, rows, cols, size):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.size = size
        self.cells = [[0 for j in range(cols)] for i in range(rows)]
        self.create_cells()

    def create_cells(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = tk.Canvas(self.master, width=self.size, height=self.size, bg='white', highlightthickness=1, highlightbackground='gray')
                cell.grid(row=i, column=j)
                cell.bind('<Button-1>', lambda event, i=i, j=j: self.toggle_cell(i, j))

    def toggle_cell(self, row, col):
        cell = self.cells[row][col]
        if cell == 0:
            self.cells[row][col] = 1
        else:
            self.cells[row][col] = 0
        self.update_cell(row, col)

    def update_cell(self, row, col):
        cell = self.cells[row][col]
        color = 'white' if cell == 0 else 'black'
        canvas = self.master.grid_slaves(row=row, column=col)[0]
        canvas.configure(bg=color)

root = tk.Tk()
grid = CellGrid(root, 10, 10, 30)
root.mainloop()
