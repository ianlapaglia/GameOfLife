# Game of Life

## Description
This project is an interactive Game of Life simulation built using Python and Tkinter. Users can create and modify a grid of cells, run or pause the simulation, adjust settings, and save or load board configurations.

## Requirements
- Python 3 installed
- Visual Studio Code (VS Code)
- Python extension for VS Code
- Tkinter (usually included with Python)

No additional third-party Python libraries are required.

## How to Run the Program

1. Download or clone the project repository.
2. Open the project folder in Visual Studio Code.
3. Make sure the following files are in the same folder:
   - `Board.py`
   - `game.py`
   - `UserInterface.py`
4. Open `UserInterface.py` in VS Code.
5. Click the **Run Python File** button (play icon) in the upper-right corner of VS Code.
6. The Game of Life application window should open.

Alternatively, run the following command in the VS Code terminal:

```bash
python UserInterface.py
```

If `python` does not work, try:

```bash
py UserInterface.py
```

## How to Use

- **Play/Pause:** Starts or pauses the simulation.
- **Set:** Applies the entered board dimensions, speed, cell size, and birth/survival rules.
- **Randomize:** Generates a random arrangement of living and dead cells.
- **Clear:** Resets the board to empty.
- **Save:** Saves the current board configuration to a `.txt` file.
- **Load:** Loads a previously saved board configuration.
- **Quit:** Closes the application.

Users can also click individual cells to change them between alive (black) and dead (white) while the simulation is paused.

## Additional Notes
- The default board size is 10 rows by 10 columns.
- Board dimensions must be between 1 and 100.
- The default simulation speed is 100 milliseconds per generation.
- The default rules are B3/S23.
- The program must be launched from `UserInterface.py`, not `Board.py` or `game.py`. or game.py.
