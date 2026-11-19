"""
Authors: Jacob McFadden,
Description: Game class for interactive cellular automaton with board configuration, B/S rules, randomization, pause/continue and save/load.
Date: Nov 2026
"""
from Board import Board, Cell
import random
import tkinter as tk

class Game:
    def __init__(self, renderCallback=None, afterCallback=None, row=10, column=10):
        self.board = Board(row, column)
        self.isRunning = False
        self.interval = 100  # Milliseconds between generations
        self.renderCallback = renderCallback
        self.after = afterCallback  # Tk root.after, injected by the UI
        self.root = None  # Tk root, supplied by UI for cancellation
        self._scheduled = None

    def render(self):
        # An optional callback permits model testing without a display.
        if self.renderCallback is not None:
            self.renderCallback()

    def makeEmptyBoard(self, row, column):
        self.stopGame()
        old_rule = self.board.BSRule
        self.board = Board(row, column)
        self.board.BSRule = old_rule
        self.render()

    def runGame(self):
        if self.isRunning:
            return
        self.isRunning = True
        self.runIteration()

    def stopGame(self):
        self.isRunning = False
        if self._scheduled is not None and self.root is not None:
            try:
                self.root.after_cancel(self._scheduled)
            except (tk.TclError, ValueError):
                pass
        self._scheduled = None

    def runIteration(self):
        if not self.isRunning:
            return
        newMatrix = []
        for row in range(self.board.rows):
            newRow = []
            for column in range(self.board.columns):
                neighbors = self.board.calculateNeighbors(row, column)
                newRow.append(self.board.getNextState(row, column, neighbors))
            newMatrix.append(newRow)
        # Apply states simultaneously: earlier changes must not affect later counts.
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                self.board.matrix[row][column].setState(newMatrix[row][column])
        self.render()
        if self.isRunning and self.after is not None:
            self._scheduled = self.after(self.interval, self.runIteration)

    def saveToFile(self, fileName):
        try:
            with open(fileName, 'w') as file:
                file.write(f'{self.board.rows} {self.board.columns} '
                           f'{self.board.BSRule[0]} {self.board.BSRule[1]}\n')
                for row in self.board.matrix:
                    file.write(''.join(str(int(cell.getState())) for cell in row) + '\n')
            return True
        except OSError:
            return False

    def loadFromFile(self, fileName):
        try:
            with open(fileName, 'r') as file:
                header = file.readline().split()
                if len(header) != 4:
                    return False
                rows, columns = int(header[0]), int(header[1])
                born, survive = header[2], header[3]
                if any(ch not in '012345678' for ch in born + survive):
                    return False
                board = Board(rows, columns)
                states = ''.join(file.read().split())
                if len(states) != rows * columns or any(c not in '01' for c in states):
                    return False
                board.BSRule = (born, survive)
                for row in range(rows):
                    for column in range(columns):
                        board.matrix[row][column].setState(states[row * columns + column] == '1')
        except (OSError, ValueError, TypeError):
            return False
        # Preserve the current board if loading fails.
        self.stopGame()
        self.board = board
        self.render()
        return True

    def toggleCell(self, row, column):
        if self.isRunning:
            return False
        changed = self.board.toggleCell(row, column)
        if changed:
            self.render()
        return changed

    def setBSRule(self, BSRule):
        born, survive = BSRule
        born, survive = str(born), str(survive)
        if any(c not in '012345678' for c in born + survive):
            raise ValueError('B/S rules must contain only digits 0 through 8.')
        if not born or not survive:
            raise ValueError('Both birth and survival rules are required.')
        self.stopGame()
        self.board.BSRule = (born, survive)

    def randomizeBoard(self):
        self.stopGame()
        for row in self.board.matrix:
            for cell in row:
                cell.setState(random.choice([True, False]))
        self.render()
