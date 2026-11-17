"""
Authors: Amy Perez, Jacob McFadden
Description: Cell and Board class for interactive cellular automaton with alterable states, neighbor calculation, and next state calculation
"""

class Cell:
    #True means alive, and False means dead
    def __init__(self, state: bool = False):
        self.state = bool(state)

    def toggleCell(self) -> None:
        self.state = not self.state

    def setState(self, newState: bool) -> None:
        self.state = bool(newState)

    def getState(self) -> bool:
        return self.state


class Board:
    def __init__(self, rows: int = 10, columns: int = 20):
        if rows < 1 or columns < 1:
            raise ValueError("Board dimensions must be positive.")

        self.rows = int(rows)
        self.columns = int(columns)
        self.BSRules = {"born": {3}, "survive": {2,3}}
        self.matrix = [[Cell(False) for _ in range(self.columns)] for _ in range(self.rows)]

    def calculateNeighbors(self, row: int, column: int) -> int:
        count = 0
        for row_offset in (-1, 0, 1):
            for column_offset in (-1, 0, 1):
                if row_offset == 0 and column_offset == 0:
                    continue
                neighbor_row = row + row_offset
                neighbor_column = column + column_offset
                if (0 <= neighbor_row < self.rows and 0 <= neighbor_column < self.columns):
                    if self.matrix[neighbor_row][neighbor_column].getState():
                        count += 1
        return count

    def getNextState(self, row, column, neighbors) -> bool:
        currentState = self.matrix[row][column].getState()
        if currentState :
            #to separate "23" into 2 and 3
            for char in self.BSRules[1]:
                if int(char) ==neighbors :
                    return True
            return False
        else :
            for char in self.BSRules[0]:
                if int(char) == neighbors :
                    return True
            return False

    def toggleCell(self, row: int, column: int) -> None:
        if not 0 <= row < self.rows and 0 <= column < self.columns:
            return
        self.matrix[row][column].toggleCell()
