"""
Authors: Jacob McFadden,
Description: Game class for interactive cellular automaton with board configuration, B/S rules, randomization, pause/continue and save/load.
"""
from Board import Board, Cell
import random

class Game:
    def __init__(self, renderCallback, afterCallback row=10, column=10):
        self.board = Board(row,column)
        self.isRunning = False
        self.interval = 100
        self.renderCallback = renderCallback
        self.after = afterCallback
    def makeEmptyBoard(self, row, column):
        self.isRunning = False
        self.board = Board(row, column)
    def runGame(self):
        if self.isRunning :
            return
        self.isRunning = True
        self.runIteration()
    def runIteration(self) :
        if not self.isRunning :
            return
        newMatrix = []
        for row in range(self.board.rows):
            newRow = []
            for column in range(self.board.columns):
                neighbors = self.board.calculateNeighbors(row, column)
                newRow.append(self.board.getNextState(row, column, neighbors))
            newMatrix.append(newRow)
        
        for row in range(self.board.rows):
            for column in range(self.board.columns):
                self.board.matrix[row][column].setState(newMatrix[row][column])
        self.renderCallback()
        #if isRunning is false it will return. 
        self.after(self.interval, self.runIteration)
    def saveToFile(self, fileName) :
        try :
            with open(fileName, "w") as file :
                file.write(str(self.board.rows) + " " + str(self.board.columns) + " " + self.board.BSRules[0] + " " self.board.BSRules[1] + " ")
                for row in self.board.matrix :
                    for cell in row :
                        file.write(str(int(cell.getState())))
            return True
        except OSError :
            return False

    def loadFromFile(self,fileName) :
        self.stopGame()
        try :
            with open(fileName, "r") as file :
                data = file.read().split()
                self.board.rows = data[0]
                self.board.columns = data[1]
                self.board.BSRules = (data[2], data[3])
                states = data[3]
                if len(states) == rows*columns :
                    for row in range(self.board.rows) :
                        for column in range(self.board.columns) :
                            self.board.matrix[row][column].setState(states[row*self.board.columns+column] == "1")
                else :
                    return False
            return True

        except OSError :
            return False

    def toggleCell(self,row, column) :
        if row > self.board.rows and column > self.board.columns :
            return False
        self.board.toggleCell(row,column)
    
    def setBSRule(self, BSRule) :
        self.stopGame()
        self.BSRules = BSRule

    def randomizeBoard(self) :
        self.stopGame()
        for row in self.board.matrix :
            for cell in row :
                cell.setState(random.choice([True, False]))
        self.renderCallback()


