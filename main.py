import tkinter as tk
import json
import random
from tkinter import filedialog

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
MAX_FPS = 60

root = tk.Tk()
root.title("Conway's Game of Life")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

grid = [[0 for y in range(HEIGHT // CELL_SIZE)] for x in range(WIDTH // CELL_SIZE)]
is_running = True

def count_neighbors(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if 0 <= x + i < len(grid) and 0 <= y + j < len(grid[0]) and grid[x + i][y + j]:
                count += 1
    return count

def update():
    global grid
    new_grid = [[0 for y in range(len(grid[0]))] for x in range(len(grid))]
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            count = count_neighbors(x, y)
            if grid[x][y] and count in (2, 3):
                new_grid[x][y] = 1
            elif not grid[x][y] and count == 3:
                new_grid[x][y] = 1
    grid = new_grid
    draw()

def draw():
    canvas.delete("all")
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y]:
                canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill="black")

def toggle_cell(event):
    global grid
    x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
    grid[x][y] = 1 - grid[x][y]
    draw()

def drag_cell(event):
    global grid
    x, y = event.x // CELL_SIZE, event.y // CELL_SIZE
    grid[x][y] = 1
    draw()

def clear_grid():
    global grid
    grid = [[0 for y in range(len(grid[0]))] for x in range(len(grid))]
    draw()

def start():
    global is_running
    is_running = True
    run()

def stop():
    global is_running
    is_running = False

def run():
    if is_running:
        update()
        root.after(1000 // MAX_FPS, run)

def randomize():
    global grid
    grid = [[random.randint(0, 1) for y in range(len(grid[0]))] for x in range(len(grid))]
    draw()

def set_speed(fps):
    global MAX_FPS
    MAX_FPS = fps

def save_pattern():
    global grid
    pattern = {"grid": grid}
    file_path = filedialog.asksaveasfilename(defaultextension=".json")
    if file_path:
        with open(file_path, "w") as f:
            json.dump(pattern, f)
            print("Pattern saved.")

def open_pattern():
    global grid
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as f:
            pattern = json.load(f)
            grid = pattern["grid"]
            draw()
            print("Pattern loaded.")

# Create buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

start_button = tk.Button(button_frame, text="Start", command=start)
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(button_frame, text="Stop", command=stop)
stop_button.pack(side=tk.LEFT)

clear_button = tk.Button(button_frame, text="Clear", command=clear_grid)
clear_button.pack(side=tk.LEFT)

randomize_button = tk.Button(button_frame, text="Randomize", command=randomize)
randomize_button.pack(side=tk.LEFT)

speed_label = tk.Label(button_frame, text="Speed:")
speed_label.pack(side=tk.LEFT)

save_button = tk.Button(button_frame, text="Save", command=save_pattern)
save_button.pack(side=tk.LEFT)

open_button = tk.Button(button_frame, text="Open", command=open_pattern)
open_button.pack(side=tk.LEFT)

speed_5_button = tk.Button(button_frame, text="5 FPS", command=lambda: set_speed(5))
speed_5_button.pack(side=tk.LEFT)

speed_10_button = tk.Button(button_frame, text="10 FPS", command=lambda: set_speed(10))
speed_10_button.pack(side=tk.LEFT)

speed_20_button = tk.Button(button_frame, text="20 FPS", command=lambda: set_speed(20))
speed_20_button.pack(side=tk.LEFT)

speed_30_button = tk.Button(button_frame, text="30 FPS", command=lambda: set_speed(30))
speed_30_button.pack(side=tk.LEFT)

speed_60_button = tk.Button(button_frame, text="60 FPS", command=lambda: set_speed(60))
speed_60_button.pack(side=tk.LEFT)

canvas.bind("<Button-1>", toggle_cell)
canvas.bind("<B1-Motion>", drag_cell)

root.mainloop() 
