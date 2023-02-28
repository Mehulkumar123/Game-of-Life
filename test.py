import tkinter as tk
import random
import pickle

# Global constants
CELL_SIZE = 10
GRID_WIDTH = 60
GRID_HEIGHT = 40
INITIAL_LIVE_CELLS = 800
SIMULATION_SPEED = 10 # iterations per second

# Global variables
cells = None
root = None
canvas = None
pause_button = None
clear_button = None
speed_scale = None
iteration = 0
paused = False
random_button = None

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = False
        self.rect = None
    
    def create_rect(self):
        x0 = self.x * CELL_SIZE
        y0 = self.y * CELL_SIZE
        x1 = (self.x + 1) * CELL_SIZE
        y1 = (self.y + 1) * CELL_SIZE
        self.rect = canvas.create_rectangle(x0, y0, x1, y1, fill='white')
    
    def change_colour(self):
        self.alive = not self.alive
        fill_colour = 'black' if self.alive else 'white'
        canvas.itemconfig(self.rect, fill=fill_colour)
    
    def change_state(self, neighbors):
        count = sum([1 for n in neighbors if n.alive])
        if self.alive:
            if count < 2 or count > 3:
                self.alive = False
        else:
            if count == 3:
                self.alive = True

def create_grid():
    global cells
    cells = [[Cell(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cells[x][y].create_rect()

def change_colour(event):
    x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
    cells[x][y].change_colour()

def change_cell_state():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            neighbors = [cells[(x+i) % GRID_WIDTH][(y+j) % GRID_HEIGHT] for i in (-1, 0, 1) for j in (-1, 0, 1) if not i == j == 0]
            cells[x][y].change_state(neighbors)

def start_game():
    global iteration
    change_cell_state()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            fill_colour = 'black' if cells[x][y].alive else 'white'
            canvas.itemconfig(cells[x][y].rect, fill=fill_colour)
    canvas.create_text(50, GRID_HEIGHT*CELL_SIZE+10, text="Iteration {}".format(iteration))
    canvas.update()
    iteration += 1
    if not paused:
        root.after(1000 // SIMULATION_SPEED, start_game)

def pause_game():
    global paused
    paused = not paused
    if paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        start_game()

def clear():
    global iteration, paused
    iteration = 0
    paused = False
    create_grid()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cells[x][y].alive = False
            fill_colour = 'white'
            canvas.itemconfig(cells[x][y].rect, fill=fill_colour)
    pause_button.config(text='Pause')


def change_colour(self):
    self.alive = not self.alive
    fill_colour = 'black' if self.alive else 'white'
    canvas.itemconfig(self.rect, fill=fill_colour)

def change_state(self, neighbors):
    count = sum([1 for n in neighbors if n.alive])
    if self.alive:
        if count < 2 or count > 3:
            self.alive = False
    else:
        if count == 3:
            self.alive = True

def create_grid():
    global cells
    cells = [[Cell(x, y) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cells[x][y].create_rect()

def change_colour(event):
    x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
    cells[x][y].change_colour()

def change_cell_state():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            neighbors = [cells[(x+i) % GRID_WIDTH][(y+j) % GRID_HEIGHT] for i in (-1, 0, 1) for j in (-1, 0, 1) if not i == j == 0]
            cells[x][y].change_state(neighbors)

def start_game():
    global iteration
    change_cell_state()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            fill_colour = 'black' if cells[x][y].alive else 'white'
            canvas.itemconfig(cells[x][y].rect, fill=fill_colour)
    canvas.create_text(50, GRID_HEIGHT*CELL_SIZE+10, text="Iteration {}".format(iteration))
    canvas.update()
    iteration += 1
    if not paused:
        root.after(1000 // SIMULATION_SPEED, start_game)

def pause_game():
    global paused
    paused = not paused
    if paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
    start_game()

def exit_game():
    root.destroy()

def reset():
    global iteration, paused
    iteration = 0
    paused = False
    create_grid()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cells[x][y].alive = False
            fill_colour = 'white'
            canvas.itemconfig(cells[x][y].rect, fill=fill_colour)
    pause_button.config(text="Pause")

def create_live_cells():
    live_cells = random.sample(range(GRID_WIDTH * GRID_HEIGHT), INITIAL_LIVE_CELLS)
    for i in live_cells:
        x = i % GRID_WIDTH
        y = i // GRID_WIDTH
        cells[x][y].alive = True
        fill_colour = 'black'
        canvas.itemconfig(cells[x][y].rect, fill=fill_colour)

def save_game():
    with open("game_of_life_save.pkl", "wb") as f:
        pickle.dump(cells, f)

def load_game():
    global cells, iteration
    with open("game_of_life_save.pkl", "rb") as f:
        cells = pickle.load(f)
    create_grid()
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            fill_colour = 'black' if cells[x][y].alive else 'white'
            canvas.itemconfig(cells[x][y].rect, fill=fill_colour)
    iteration = 0

def randomise():
    global cells, iteration
    create_grid()
    for x in range(INITIAL_LIVE_CELLS):
        rx = random.randint(0, GRID_WIDTH-1)
        ry = random.randint(0, GRID_HEIGHT-1)
        cells[rx][ry].alive = True
        fill_colour = 'black' if cells[rx][ry].alive else 'white'
        canvas.itemconfig(cells[rx][ry].rect, fill=fill_colour)
    iteration = 0

def set_simulation_speed(speed):
    global SIMULATION_SPEED
    SIMULATION_SPEED = int(speed)

# Main code
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Conway's Game of Life")
    canvas = tk.Canvas(root, width=GRID_WIDTH*CELL_SIZE, height=GRID_HEIGHT*CELL_SIZE)
    canvas.pack()
    create_grid()
    canvas.bind("<Button-1>", change_colour)
    tk.Button(root, text="Start", command=start_game).pack(side=tk.LEFT)
    pause_button = tk.Button(root, text="Pause", command=pause_game)
    pause_button.pack(side=tk.LEFT)
    clear_button = tk.Button(root, text="Clear", command=clear)
    clear_button.pack(side=tk.LEFT)
    tk.Button(root, text="Exit", command=exit_game).pack(side=tk.LEFT)
    tk.Button(root, text="Save", command=save_game).pack(side=tk.LEFT)
    tk.Button(root, text="Load", command=load_game).pack(side=tk.LEFT)
    random_button = tk.Button(root, text="Randomise", command=randomise)
    random_button.pack(side=tk.LEFT)
    speed_scale = tk.Scale(root, from_=1, to=30, orient=tk.HORIZONTAL, label="Speed", command=set_simulation_speed)
    speed_scale.set(SIMULATION_SPEED)
    speed_scale.pack(side=tk.LEFT)
    root.mainloop()
