"""
Authors: Amy Perez, Jacob McFadden
Description: Cell and Board class for interactive cellular automaton with alterable states, neighbor calculation, and next state calculation
"""

class Cell:
    #True means alive, and False means dead
    def __init__(self, state: bool = False):
        self.state = bool(state)

    def toggleCell(self):
        self.state = not self.state

    def setState(self, newState: bool):
        self.state = bool(newState)

    def getState(self) -> bool:
        return self.state


class Board:
    def __init__(self, rows: int = 30, columns: int = 40):
        if not 1 <= rows <= 100 or not 1 <= columns <= 100:
            raise ValueError("Rows and columns must be between 1 and 100.")
        self.rows, self.columns = rows, columns
        self.BSRule = ("3", "23")# B3/S23 by default
        self.matrix = [[Cell() for _ in range(columns)] for _ in range(rows)]

    
    def calculateNeighbors(self, row: int, column: int) -> int:
        #Count the eight neighboring positions; edges do not wrap
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
            for char in self.BSRule[1]:
                if int(char) ==neighbors :
                    return True
            return False
        else:
            for char in self.BSRule[0]:
                if int(char) == neighbors :
                    return True
            return False

    def toggleCell(self, row: int, column: int) -> bool:
        if not 0 <= row < self.rows and 0 <= column < self.columns:
            return False
        self.matrix[row][column].toggleCell()
        return True
