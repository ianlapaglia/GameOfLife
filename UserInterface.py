#Authors: Amy Perez,
#Description: Interactive cellular automaton with board configuration, B/S rules, randomization, pause/continue, and JSON save/load.


class UserInterface:
  def __init__(self,root):
    self.root = root
    self.root.title("Game of Life")
    #cellSize can be changed if necessary to make it easier to test
    self.cellSize = 18
    #Call the game class
    
