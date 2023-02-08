#!/usr/bin/python3
# B351/Q351 SP 2022
# Do not share these assignments or their solutions outside of this class.

import csv
import itertools

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        # initialize all of the variables
        self.n2 = 0
        self.n = 0
        self.spaces = 0
        self.board = None
        self.valsInRows = None
        self.valsInCols = None
        self.valsInBoxes = None
        self.unsolvedSpaces = None

        # load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    # loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                # Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valsInRows = [set() for _ in range(self.n2)]
                        self.valsInCols = [set() for _ in range(self.n2)]
                        self.valsInBoxes = [set() for _ in range(self.n2)]
                        self.unsolvedSpaces = set(itertools.product(range(self.n2), range(self.n2)))

                # check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row must have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                # add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valsInRows[reader.line_num-1].add(int(item))
                        self.valsInCols[index].add(int(item))
                        self.valsInBoxes[self.spaceToBox(reader.line_num-1, index)].add(int(item))
                        self.unsolvedSpaces.remove((reader.line_num-1, index))


    ##########################################
    ####   Utility Functions
    ##########################################

    # converts a given row and column to its inner box number
    def spaceToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n

    # prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            # add row divider
            if r % self.n == 0 and not r == 0:
                if self.n2 > 9:
                    print("  " + "----" * self.n2)
                else:
                    print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                # add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                # add value placeholder
                if self.n2 > 9:
                    if val is None: row += "__"
                    else: row += "%2i" % val
                else:
                    if val is None: row += "_"
                    else: row += str(val)
            print(row)


    ##########################################
    ####   Move Functions - YOUR IMPLEMENTATIONS GO HERE
    ##########################################

    # makes a move, records it in its row, col, and box, and removes the space from unsolvedSpaces
    def makeMove(self, space, value):

        if(self.isValidMove(space, value)):
            self.valsInBoxes[self.spaceToBox(space[0], space[1])] = value
            self.valsInRows[space[0]] = value
            self.valsInCols[space[1]] = value
            self.unsolvedSpaces.remove(space)
            self.board[space] = value

    # removes the move, its record in its row, col, and box, and adds the space back to unsolvedSpaces
    def undoMove(self, space, value):
        self.valsInBoxes[self.spaceToBox(space[0], space[1])] = None
        self.valsInRows[space[0]] = None
        self.valsInCols[space[1]] = None
        self.unsolvedSpaces.add(space)
        self.board.__delitem__(space)

    # returns True if the space is empty and on the board,
    # and assigning value to it if not blocked by any constraints
    def isValidMove(self, space, value):

        for s in self.unsolvedSpaces:

            if(space == s):

                for v in self.valsInRows[space[0]]:

                    if(v == value):
                        return False
                    
                for v in self.valsInCols[space[1]]:

                    if(v == value):
                        return False
                    
                for v in self.valsInBoxes[self.spaceToBox(space[0], space[1])]:

                    if(v == value):
                        return False
                    
                if(space[0] < 0 or space[1] < 0):
                    return False
         
                return True
            
        return False

    # optional helper function for use by getMostConstrainedUnsolvedSpace
    def evaluateSpace(self, space):

        val = 0

        spacesVisited = []
                
        for v in self.valsInBoxes[self.spaceToBox(space[0], space[1])]:
            spacesVisited.append(v)
            val+=1
            
        for r in self.valsInRows[space[0]]:
            if r not in spacesVisited:
                val+=1
                spacesVisited.append(r)
                
        for c in self.valsInCols[space[1]]:
            if c not in spacesVisited:
                val+=1

        return val

    # gets the unsolved space with the most current constraints
    # returns None if unsolvedSpaces is empty
    def getMostConstrainedUnsolvedSpace(self):

        mostConstrainedValue = 0
        mostConstrainedSpace = None

        if(len(self.unsolvedSpaces) > 0):

            for s in self.unsolvedSpaces:

                currentCheck = self.evaluateSpace(s)

                if(currentCheck > mostConstrainedValue):

                    mostConstrainedValue = currentCheck
                    mostConstrainedSpace = s
                
            return mostConstrainedSpace
        
        return None

class Solver:
    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self):
        pass

    ##########################################
    ####   Solver
    ##########################################

    # recursively selects the most constrained unsolved space and attempts
    # to assign a value to it

    # upon completion, it will leave the board in the solved state (or original
    # state if a solution does not exist)

    # returns True if a solution exists and False if one does not
    def solveBoard(self, board):
        raise NotImplementedError


if __name__ == "__main__":
    # change this to the input file that you'd like to test
    board = Board('C:/Users/jbluk/OneDrive/Documents/IU/Spring 2023/Intro to AI/HW2P/test_a2/test_a2/data/tests/invalid-boards/06.csv')
    s = Solver()
    s.solveBoard(board)
    board.print()
