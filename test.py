import tkinter as tk
import random

# Global constants
CELL_SIZE = 10
GRID_WIDTH = 60
GRID_HEIGHT = 40
INITIAL_LIVE_CELLS = 800
SIMULATION_SPEED = 10  # iterations per second

# Global variables
cells = None
root = None
canvas = None
pause_button = None
restart_button = None
speed_scale = None
iteration = 0
paused = False


def init_cells():
    """Initialize the grid of cells."""
    global cells
    cells = [[random.randint(0, 1) for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]


def draw_cells():
    """Draw the current state of the grid."""
    global iteration
    canvas.delete("all")
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if cells[x][y] == 1:
                canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE,
                                        (x+1)*CELL_SIZE, (y+1)*CELL_SIZE,
                                        fill="black")
    canvas.create_text(50, GRID_HEIGHT*CELL_SIZE+10,
                       text="Iteration {}".format(iteration))
    canvas.update()


def count_neighbors(x, y):
    """Count the number of live neighbors around the given cell."""
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (x+i) < 0 or (x+i) >= GRID_WIDTH or (y+j) < 0 or (y+j) >= GRID_HEIGHT:
                continue
            count += cells[x+i][y+j]
    return count


def step():
    """Compute the next state of the grid."""
    global cells, iteration
    new_cells = [[0 for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            count = count_neighbors(x, y)
            if cells[x][y] == 1 and (count == 2 or count == 3):
                new_cells[x][y] = 1
            elif cells[x][y] == 0 and count == 3:
                new_cells[x][y] = 1
    cells = new_cells
    iteration += 1


def run():
    """Run the simulation."""
    global paused
    if not paused:
        step()
        draw_cells()
    root.after(1000 // SIMULATION_SPEED, run)


def pause():
    """Pause or resume the simulation."""
    global paused
    paused = not paused
    if paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        run()


def restart():
    """Restart the simulation."""
    global iteration, paused
    iteration = 0
    paused = False
    init_cells()
    draw_cells()
    pause_button.config(text="Pause")


def change_speed(value):
    """Change the speed of the simulation."""
    global SIMULATION_SPEED
    SIMULATION_SPEED = int(value)

def main():
    """Initialize the GUI and start the simulation."""
    global root, canvas, pause_button, restart_button, speed_scale
    root = tk.Tk()
    root.title("Game of Life")

    canvas = tk.Canvas(root, width=GRID_WIDTH*CELL_SIZE,
                       height=(GRID_HEIGHT*CELL_SIZE)+30)
    canvas.pack()

    # Add a button to pause/resume the simulation
    pause_button = tk.Button(root, text="Pause", command=pause)
    pause_button.pack(side=tk.LEFT)

    # Add a button to restart the simulation
    restart_button = tk.Button(root, text="Restart", command=restart)
    restart_button.pack(side=tk.LEFT)

    # Add a scale to control the simulation speed
    speed_scale = tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL,
                           label="Speed", command=change_speed)
    speed_scale.set(SIMULATION_SPEED)
    speed_scale.pack(side=tk.RIGHT)

    # Initialize the grid of cells
    init_cells()

    # Draw the initial state of the grid
    draw_cells()

    # Start the simulation
    run()

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
