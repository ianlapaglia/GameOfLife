#Authors: Amy Perez,
#Description: Interactive cellular automaton with board configuration, B/S rules, randomization, pause/continue, and JSON save/load.

import tkinter as tk
from tkinter import messagebox, filedialog
#use GameOfLife.py along with the UI
from game import game

class UserInterface:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Game of Life')
        self.cellSize = 18
        self.game = Game(renderCallback=self.render, afterCallback=root.after)
        self.game.root = root

        settings = tk.Frame(root, padx=8, pady=8)
        settings.pack()
        self.rowsEntry = self._entry(settings, 'Rows', '40', 0)
        self.columnsEntry = self._entry(settings, 'Columns', '40', 2)
        self.tickEntry = self._entry(settings, 'Tick (ms)', '100', 4)
        self.cellEntry = self._entry(settings, 'Cell size', '18', 6)
        self.bornEntry = self._entry(settings, 'Born', '3', 8)
        self.surviveEntry = self._entry(settings, 'Survive', '23', 10)

        controls = tk.Frame(root, padx=8, pady=4)
        controls.pack()
        self.playButton = tk.Button(controls, text='Play', command=self.playToggleOnClick)
        self.playButton.pack(side=tk.LEFT)
        for label, callback in [('Set', self.setOnClick),
                                ('Randomize', self.randomizeOnClick),
                                ('Clear', self.clearOnClick),
                                ('Save', self.saveOnClick),
                                ('Load', self.loadOnClick),
                                ('Quit', self.quitOnClick)]:
            tk.Button(controls, text=label, command=callback).pack(side=tk.LEFT)
        self.canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.canvas.pack(padx=8, pady=8)
        self.canvas.bind('<Button-1>', self.handleClick)
        root.protocol('WM_DELETE_WINDOW', self.quitOnClick)
        self.render()

    def _entry(self, parent, label, value, column):
        tk.Label(parent, text=label).grid(row=0, column=column)
        entry = tk.Entry(parent, width=5)
        entry.insert(0, value)
        entry.grid(row=0, column=column + 1)
        return entry

    def render(self):
        board = self.game.board
        self.canvas.config(width=board.columns * self.cellSize,
                           height=board.rows * self.cellSize)
        self.canvas.delete('all')
        for row in range(board.rows):
            for column in range(board.columns):
                x, y = column * self.cellSize, row * self.cellSize
                fill = 'black' if board.matrix[row][column].getState() else 'white'
                self.canvas.create_rectangle(x, y, x + self.cellSize,
                                             y + self.cellSize,
                                             fill=fill, outline='#cccccc')

    def handleClick(self, event):
        row = event.y // self.cellSize
        column = event.x // self.cellSize
        self.game.toggleCell(row, column)

    def playToggleOnClick(self):
        if self.game.isRunning:
            self.game.stopGame()
            self.playButton.config(text='Play')
        else:
            self.game.runGame()
            self.playButton.config(text='Pause')

    def setOnClick(self):
        try:
            rows, columns = int(self.rowsEntry.get()), int(self.columnsEntry.get())
            tick, size = int(self.tickEntry.get()), int(self.cellEntry.get())
            if tick < 1 or not 4 <= size <= 40:
                raise ValueError('Tick must be positive; cell size must be 4–40.')
            # Validate dimensions and rules before modifying the current game.
            from Board import Board
            Board(rows, columns)
            born, survive = self.bornEntry.get(), self.surviveEntry.get()
            if not born or not survive or any(ch not in '012345678' for ch in born + survive):
                raise ValueError('Birth/survival rules must use digits 0–8.')
            self.game.makeEmptyBoard(rows, columns)
            self.game.setBSRule((born, survive))
            self.game.interval = tick
            self.cellSize = size
            self.playButton.config(text='Play')
            self.render()
        except ValueError as error:
            messagebox.showerror('Invalid settings', str(error))

    def saveOnClick(self):
        fileName = filedialog.asksaveasfilename(defaultextension='.txt',
                                                filetypes=[('Life text files', '*.txt')])
        if fileName and not self.game.saveToFile(fileName):
            messagebox.showerror('Save error', 'Unable to save the board.')

    def loadOnClick(self):
        fileName = filedialog.askopenfilename(filetypes=[('Life text files', '*.txt'),
                                                          ('All files', '*.*')])
        if fileName and not self.game.loadFromFile(fileName):
            messagebox.showerror('Load error', 'Invalid or unreadable board file.')
        elif fileName:
            self.playButton.config(text='Play')
            board = self.game.board
            for entry, value in [(self.rowsEntry, board.rows),
                                 (self.columnsEntry, board.columns),
                                 (self.bornEntry, board.BSRule[0]),
                                 (self.surviveEntry, board.BSRule[1])]:
                entry.delete(0, tk.END)
                entry.insert(0, str(value))

    def randomizeOnClick(self):
        self.game.randomizeBoard()
        self.playButton.config(text='Play')

    def clearOnClick(self):
        self.game.makeEmptyBoard(self.game.board.rows, self.game.board.columns)
        self.playButton.config(text='Play')

    def quitOnClick(self):
        self.game.stopGame()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    UserInterface(root)
    root.mainloop()
