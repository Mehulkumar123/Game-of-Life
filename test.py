import tkinter as tk
import random

class Cell:
    def __init__(self, x, y, size, canvas):
        self.x = x
        self.y = y
        self.size = size
        self.canvas = canvas
        self.state = 0
        self.id = canvas.create_rectangle(x*size, y*size, (x+1)*size, (y+1)*size, fill='white')
    
    def toggle(self):
        self.state = 1 - self.state
        if self.state == 1:
            self.canvas.itemconfig(self.id, fill='green')
        else:
            self.canvas.itemconfig(self.id, fill='white')

class GameOfLife:
    def __init__(self, rows, cols, cell_size=10, game_speed=10):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.game_speed = game_speed
        
        self.root = tk.Tk()
        self.root.title("Conway's Game of Life")
        
        self.canvas = tk.Canvas(self.root, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()
        
        self.grid = [[Cell(i, j, cell_size, self.canvas) for j in range(cols)] for i in range(rows)]
        
        self.canvas.bind("<Button-1>", self.changeColour)
        
        self.start_button = tk.Button(self.root, text="Start", command=self.startGame)
        self.start_button.pack(side=tk.LEFT)
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pauseGame)
        self.pause_button.pack(side=tk.LEFT)
        self.step_button = tk.Button(self.root, text="Step", command=self.stepGame)
        self.step_button.pack(side=tk.LEFT)
        
        self.speed_slider = tk.Scale(self.root, from_=1, to=20, orient=tk.HORIZONTAL, label="Speed", command=self.setSpeed)
        self.speed_slider.pack()
        
        self.begin_id = None
        
        self.randomizeGrid()
        
        self.root.mainloop()
    
    def changeColour(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.grid[x][y].toggle()

    def changeCellState(self, x, y):
        alive_neighbors = 0
        for i in range(max(0, x-1), min(self.rows, x+2)):
            for j in range(max(0, y-1), min(self.cols, y+2)):
                if i == x and j == y:
                    continue
                alive_neighbors += self.grid[i][j].state
        if self.grid[x][y].state == 1:
            if alive_neighbors in (2, 3):
                return 1
            else:
                return 0
        else:
            if alive_neighbors == 3:
                return 1
            else:
                return 0
    
    def startGame(self):
        if self.begin_id is not None:
            return
        self.stepGame()
        self.begin_id = self.root.after(int(1000 / self.game_speed), self.startGame)
    
    def pauseGame(self):
        if self.begin_id is not None:
            self.root.after_cancel(self.begin_id)
            self.begin_id = None
    
    def stepGame(self):
        next_state = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                next_state[i][j] = self.changeCellState(i, j)
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j].state = next_state[i][j]
                if self.grid[i][j].state == 1:
                    self.canvas.itemconfig(self.grid[i][j].id, fill='green')
                else:
                    self.canvas.itemconfig(self.grid[i][j].id, fill='white')

    def randomizeGrid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < 0.5:
                    self.grid[i][j].state = 1
                    self.grid[i][j].canvas.itemconfig(self.grid[i][j].id, fill='green')

    
    def randomizeGrid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                r = random.randint(0, 1)
                self.grid[i][j].state = r
                if r == 1:
                    self.canvas.itemconfig(self.grid[i][j].id, fill='green')
                else:
                    self.canvas.itemconfig(self.grid[i][j].id, fill='white')
    
    def setSpeed(self, val):
        self.game_speed = int(val)
        if self.begin_id is not None:
            self.pauseGame()
            self.startGame()

if __name__ == '__main__':
    game = GameOfLife(50, 50)
