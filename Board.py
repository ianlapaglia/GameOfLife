"""
Authors: Amy Perez
Date: 20 November, 2026
Description: Interactive cellular automaton with board configuration, B/S rules,
randomization, pause/continue, and JSON save/load.
"""

import json
import random
import tkinter as tk
from tkinter import filedialog, messagebox

class Cell:
    def __init__(self, state: bool = False):
        self.state = bool(state)

    def toggleCell(self) -> None:
        self.state = not self.state

    def setState(self, newState: bool) -> None:
        self.state = bool(newState)

    def getState(self) -> bool:
        return self.state


class Board:
    def __init__(self, rows: int, columns: int):
        if rows < 1 or columns < 1:
            raise ValueError("Board dimensions must be positive.")

        self.rows, self.columns = rows, columns
        self.BSRules = ("3", "23")
        self.matrix = [[Cell() for _ in range(columns)] for _ in range(rows)]

    def calculateNeighbors(self, row: int, column: int) -> int:
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, column + dc
                if 0 <= r < self.rows and 0 <= c < self.columns:
                    if self.matrix[r][c].getState():
                        count += 1
        return count

    def toggleCell(self, row: int, column: int) -> None:
        if 0 <= row < self.rows and 0 <= column < self.columns:
            self.matrix[row][column].toggleCell()