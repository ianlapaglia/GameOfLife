"""
Authors: Amy Perez, Olivia Mott
Description: Interactive cellular automaton with board configuration, B/S rules, randomization, pause/continue, and JSON save/load.
Date: Nov 2026
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from game import Game

class UserInterface:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Game of Life')
        self.backgroundColor = '#1e3c72'  # dark blue
        self.textColor = 'white'
        self.root.configure(bg=self.backgroundColor)
        self.cellSize = 18
        self.game = Game(renderCallback=self.render, afterCallback=root.after)
        self.game.root = root

        self.settings = tk.Frame(root, padx=8, pady=8, bg=self.backgroundColor)
        self.rowsEntry = self._entry(self.settings, 'Rows', '10', 0)
        self.columnsEntry = self._entry(self.settings, 'Columns', '10', 2)
        self.tickEntry = self._entry(self.settings, 'Tick (ms)', '100', 4)
        self.cellEntry = self._entry(self.settings, 'Cell size', '18', 6)
        self.bornEntry = self._entry(self.settings, 'Born', '3', 8)
        self.surviveEntry = self._entry(self.settings, 'Survive', '23', 10)

        self.canvas = tk.Canvas(root, bg='white', highlightthickness=0)
        self.canvas.bind('<Button-1>', self.handleClick)

        self.controls = tk.Frame(root, padx=8, pady=12, bg=self.backgroundColor)
        self.playButton = tk.Button(self.controls, text='Play', command=self.playToggleOnClick)
        self.playButton.pack(side=tk.LEFT, padx=4)
        for label, callback in [('Set', self.setOnClick),
                                ('Randomize', self.randomizeOnClick),
                                ('Clear', self.clearOnClick),
                                ('Save', self.saveOnClick),
                                ('Load', self.loadOnClick),
                                ('Quit', self.quitOnClick)]:
            tk.Button(self.controls, text=label, command=callback).pack(side=tk.LEFT, padx=4)
        
        self._organize_layout()
        root.protocol('WM_DELETE_WINDOW', self.quitOnClick)
        self.render()

    def _organize_layout(self):
        # If board has more than 30 rows, place buttons between settings and canvas.
        # With many rows, the canvas grows tall and buttons at the bottom would be off-screen.
        rows = self.game.board.rows
        self.settings.pack_forget()
        self.controls.pack_forget()
        self.canvas.pack_forget()
        
        self.settings.pack()
        if rows > 30:
            self.controls.pack()
        self.canvas.pack(padx=8, pady=8)
        if rows <= 30:
            self.controls.pack()

    def _entry(self, parent, label, value, column):
        tk.Label(parent, text=label, bg=self.backgroundColor, fg=self.textColor).grid(row=0, column=column)
        entry = tk.Entry(parent, width=5)
        entry.insert(0, value)
        entry.grid(row=0, column=column + 1, padx=4)
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
            self._organize_layout()
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
