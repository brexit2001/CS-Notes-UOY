# Code adapted from Daniel Hernandez and Peter York's MCTS code

import numpy as np
import random

import colorama
from colorama import Fore, Back

class GameState:
    """
        A GameState represents a valid configuration of the 'state' of a game.
        For instance:
            - the position of all the active pieces on a chess board.
            - The position and velocities of all the entities in a 3D world.
        This interface presents the minimal functionality required to implement
        an MCTS-UCT algorithm for a 2 player game.        
    """

    def __init__(self):
        self.playerJustMoved = 2 # Game starts with Player 1.

    def Clone(self):
        """ 
        :returns: deep copy of this GameState
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """
        !! This is the environment's model !!
        Changes the GameState by carrying out the param move.
        :param move: (int) action taken by an agent.
        """
        self.playerJustMoved = 3 - self.playerJustMoved

    def GetMoves(self):
        """ :returns: int array with all available moves at this state
        """
        pass
        
    def IsGameOver(self):
        """ :returns: whether this GameState is a terminal state
        """
        return self.GetMoves() == []

    def GetResult(self, player):
        """ 
        :param player: (int) player which we want to see if he / she is a winner
        :returns: winner from the perspective of the param player
        """
        pass


class Connect4State(GameState):
    """
        GameState for the Connect 4 game.
        The board is represented as a 2D array (rows and columns).
        Each entry on the array can be:
            - 0 = empty    (.)
            - 1 = player 1 (X)
            - 2 = player 2 (O)
    """

    def __init__(self, width=7, height=6, connect=4):
        self.playerJustMoved = 2
        self.winner = 0 # 0 = no winner, 1 = Player 1 wins, 2 = Player 2 wins.

        self.width = width
        self.height = height
        self.connect = connect
        self.InitializeBoard()

    def InitializeBoard(self):
        """ 
        Initialises the Connect 4 gameboard.
        """
        self.board = []
        for y in range(self.width):
            self.board.append([0] * self.height)

    def Clone(self):
        """ 
        Creates a deep copy of the game state.
        NOTE: it is _really_ important that a copy is used during simulations
              Because otherwise MCTS would be operating on the real game board.
        :returns: deep copy of this GameState
        """
        st = Connect4State(width=self.width, height=self.height)
        st.playerJustMoved = self.playerJustMoved
        st.winner = self.winner
        st.board = [self.board[col][:] for col in range(self.width)]
        return st

    def DoMove(self, movecol):
        """ 
        Changes this GameState by "dropping" a chip in the column
        specified by param movecol.
        :param movecol: column over which a chip will be dropped
        """
        assert movecol >= 0 and movecol <= self.width and self.board[movecol][self.height - 1] == 0
        row = self.height - 1
        while row >= 0 and self.board[movecol][row] == 0:
            row -= 1

        row += 1

        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[movecol][row] = self.playerJustMoved
        if self.DoesMoveWin(movecol, row):
            self.winner = self.playerJustMoved
            
    def GetMoves(self):
        """
        :returns: array with all possible moves, index of columns which aren't full
        """
        if self.winner != 0:
            return []
        return [col for col in range(self.width) if self.board[col][self.height - 1] == 0]

    def DoesMoveWin(self, x, y):
        """ 
        Checks whether a newly dropped chip at position param x, param y
        wins the game.
        :param x: column index
        :param y: row index
        :returns: (boolean) True if the previous move has won the game
        """
        me = self.board[x][y]
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
            p = 1
            while self.IsOnBoard(x+p*dx, y+p*dy) and self.board[x+p*dx][y+p*dy] == me:
                p += 1
            n = 1
            while self.IsOnBoard(x-n*dx, y-n*dy) and self.board[x-n*dx][y-n*dy] == me:
                n += 1

            if p + n >= (self.connect + 1): # want (p-1) + (n-1) + 1 >= 4, or more simply p + n >- 5
                return True

        return False

    def IsOnBoard(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def GetResult(self, player):
        """ 
        :param player: (int) player which we want to see if he / she is a winner
        :returns: winner from the perspective of the param player
        """
        return player == self.winner

    def __repr__(self):
        s = ""
        for x in range(self.height - 1, -1, -1):
            for y in range(self.width):
                s += [Back.WHITE + Fore.WHITE + '.', Back.BLACK + Fore.WHITE + 'X', Back.BLACK + Fore.WHITE + 'O'][self.board[y][x]]
                s += Fore.RESET
                s += Back.RESET
            s += "\n"
        s += "\n\n\n"
        return s


def PrintGameResults(state):
    """ 
    Print match results. Function assumes match is over.
    """
    if state.winner != 0:
      if state.GetResult(state.playerJustMoved) == 1.0:
        print(str(state))
        print("Player " + str(state.playerJustMoved) + " wins!")
      else:
        print(str(state))
        print("Player " + str(3 - state.playerJustMoved) + " wins!")

    else:
        print("Nobody wins!")




def PlayGame(initialState):
    state = initialState
    while not state.IsGameOver():
        # Render
        print(str(state))
        # Capture user input
        if state.playerJustMoved == 1:
            # Player 2 turn
            move = random.choice(state.GetMoves())
        else:
            # Player 1 turn
            move = random.choice(state.GetMoves())
        # Update game state
        state.DoMove(move)

    PrintGameResults(state)


class Node:
    
    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.children = []
        self.parent = parent
        self.state = state
        self.playerJustMoved = state.playerJustMoved
        self.minmax = 0

    def UpdateMinMax(self, heuristic = None):
        minmax_values = [child.minmax for child in self.children]
        if self.children != []:
            if self.playerJustMoved == 1:
                self.minmax = max(minmax_values)
            else:
                self.minmax = min(minmax_values)
        else:
          if heuristic is not None:
            self.minmax = heuristic(self)
          else:
            if self.playerJustMoved == 1:
              self.minmax = 4
            else:
              self.minmax = -4
    
    def GetChildren(self):
        children = {}
        moves = self.state.GetMoves()
        for action in moves:
            new_state = self.state.Clone()
            new_state.DoMove(action)
            new_node = Node(action, self, new_state)
            children[action] = new_node
            self.children.append(new_node)
        return children

def BuildGameTree(root):
    root = BuildGameSubTree(root)
    return root

def BuildGameSubTree(node):
    if node.state.IsGameOver():
        node.UpdateMinMax()
        return(node)
    children = node.GetChildren()
    for child in node.children:
        child = BuildGameSubTree(child)
        child.UpdateMinMax()
    return(node)

def PlayGameMinMax(root, env):
    state = env
    current_node = BuildGameTree(root)
    while not state.IsGameOver():
        print(str(state))
        minmax_values = [child.minmax for child in current_node.children]
        if state.playerJustMoved == 1:
            indx = np.argwhere(np.array(minmax_values)==np.min(minmax_values)).flatten().tolist()
            indx = random.choice(indx)
        else:           
            indx = np.argwhere(np.array(minmax_values)==np.max(minmax_values)).flatten().tolist()
            indx = random.choice(indx)
        current_node = current_node.children[indx]
        state = current_node.state

def PlayGameMinMaxHeuristic(env, lookahead = 4):
    state = env
    root = BuildGameTreeH(state, lookahead)
    while not state.IsGameOver():
        print(str(state))
        minmax_values = [child.minmax for child in root.children]
        if state.playerJustMoved == 1:
            indx = np.argwhere(np.array(minmax_values)==np.min(minmax_values)).flatten().tolist()
            indx = random.choice(indx)
        else:           
            indx = np.argwhere(np.array(minmax_values)==np.max(minmax_values)).flatten().tolist()
            indx = random.choice(indx)
        move = root.children[indx].move
        state.DoMove(move)
        root = BuildGameTreeH(root.children[indx].state, depth=lookahead)
    PrintGameResults(state)

def BuildGameTreeH(current_state, depth = 5):
    root = Node(state = current_state)
    root = BuildGameSubTreeH(root,  depth)
    return root

def BuildGameSubTreeH(node, depth):
    if node.state.IsGameOver() or depth == 0:
        node.UpdateMinMax(heuristic)
        return(node)
    children = node.GetChildren()
    for child in node.children:
        child = BuildGameSubTreeH(child, depth - 1)
        child.UpdateMinMax(heuristic)
    return(node)

def heuristic(node):
    currentPlayer = 3 - node.playerJustMoved
    currentMax = 0

    for x in range(node.state.width):
        for y in range(node.state.height):
            me = node.state.board[x][y]
            if me == currentPlayer:
                for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1)]:
                    p = 1
                    while node.state.IsOnBoard(x+p*dx, y+p*dy) and node.state.board[x+p*dx][y+p*dy] == me:
                        p += 1
                    n = 1
                    while node.state.IsOnBoard(x-n*dx, y-n*dy) and node.state.board[x-n*dx][y-n*dy] == me:
                        n += 1
                    
                    if p + n > currentMax:
                        currentMax = p + n    
            y += 1
        x += 1
    if currentPlayer == 1:  # max
        return(currentMax)
    return(-currentMax)
    
    
env = Connect4State(width=10, height=10, connect= 4)
PlayGameMinMaxHeuristic(env, lookahead=4)
