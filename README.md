# Conway's Game of Life Simulator

This code implements Conway's Game of Life, a cellular automaton that simulates the behavior of living cells according to a set of rules. The game is played on a grid of cells, where each cell is either alive or dead.

The program uses the Tkinter library to create a graphical user interface that displays the game board and allows the user to interact with it. The board is represented by a two-dimensional list called grid, where each element is either a 0 (dead cell) or 1 (alive cell).

The rules of the game are applied to each cell on the grid during each iteration of the game. The count_neighbors function counts the number of living neighbors around each cell, and the update function updates the grid based on the rules:
|                                                       |
Any live cell with two or three live neighbors survives.
Any dead cell with three live neighbors becomes a live cell.
All other live cells die in the next generation. Similarly, all other dead cells stay dead.
The draw function uses the canvas to draw the game board, where alive cells are displayed as black rectangles.

The user can interact with the game board by clicking on cells to toggle their state, or by dragging the mouse to create live cells. The program also includes buttons to start and stop the game, clear the board, randomize the board, set the game speed, and save or load patterns.

The run function uses the after method to run the game loop at a set framerate, controlled by the MAX_FPS variable. The is_running variable is used to stop the game loop when the user clicks the "Stop" button.
