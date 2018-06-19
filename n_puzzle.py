#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 13:43:48 2018

@author: ossama
"""
import sys
# from random import shuffle
from random import randrange

allmoves = ('e', 'w', 'n', 's')


def opposite(move):
    if move == 'e':
        return 'w'
    if move == 'w':
        return 'e'
    if move == 'n':
        return 's'
    if move == 's':
        return 'n'


class Board:
    initialstate = ""
    initialdisplay = ""
    win = ""
    height = 3
    width = 3

    # initialises random board
    def __init__(self, height, width):
        Board.height = height
        Board.width = width
        self.squares = []

    def fillordered(self):
        x = [i for i in range(self.height * self.width)]
        # shuffle(x)
        for i in range(self.height * self.width):
            self.squares.append(Square(x[i], i % self.width, i // self.width))

    def randomize(self, steps):
        for i in range(steps):
            self.makerandommove()

    def makerandommove(self):
        pm = self.possiblemoves()
        randommove = pm[randrange(0, len(pm))]
        self.makemove(randommove)

    def initialize(self, state):
        x = state.split("-")
        if len(x) < self.height * self.width:
            print ("uncomplete state no initialization !")
        for i in range(self.height * self.width):
            self.squares.append(Square(int(x[i]), i % self.width, i // self.width))

    def display(self):
        disp = ""
        for i in range(self.width * self.height):
            disp += self.squares[i].toString()
            if (i + 1) % self.width == 0:
                disp += "\n"
        print (disp)

    def zerosquare(self):
        for sqr in self.squares:
            if sqr.number == 0:
                return sqr

    def state(self):
        st = ""
        for i in range(self.width * self.height):
            st += str(self.squares[i].number) + "-"
        return st

    def winstate(self):
        if (Board.win != ""):
            return Board.win
        for i in range(Board.width * Board.height):
            Board.win += str(i) + "-"
        return Board.win

    def possiblemoves(self):
        zsqr = self.zerosquare()
        moves = []
        moves.extend(allmoves)
        if zsqr.positionx == 0:
            moves.remove('e')
        if zsqr.positiony == 0:
            moves.remove('s')
        if zsqr.positionx == self.width - 1:
            moves.remove('w')
        if zsqr.positiony == self.height - 1:
            moves.remove('n')
        return moves

    def swapsquares(self, sqrindx1, sqrindx2):
        square1 = self.squares[sqrindx1]
        square2 = self.squares[sqrindx2]
        nbr = square1.number
        square1.number = square2.number
        square2.number = nbr

    # takes possible moves, not protected against bad moves
    def makemove(self, move):
        zsqr = self.zerosquare()
        zsqrindx = zsqr.positionx + self.width * zsqr.positiony
        if move == 'e':
            self.swapsquares(zsqrindx, zsqrindx - 1)
        if move == 'w':
            self.swapsquares(zsqrindx, zsqrindx + 1)
        if move == 'n':
            self.swapsquares(zsqrindx, zsqrindx + width)
        if move == 's':
            self.swapsquares(zsqrindx, zsqrindx - width)
        return self

    def makemovedboard(self, move):
        brd = Board(width, height)
        brd.initialize(self.state())
        brd.makemove(move)
        return brd

    def complexity(self):
        cmplx = 0
        for sqr in self.squares:
            cmplx += sqr.distance()
        return cmplx


class Square:

    def __init__(self, number, positionx, positiony):
        self.number = number
        self.positionx = positionx
        self.positiony = positiony

    def toString(self):
        ret = "["
        if (self.number < 10):
            ret += " "
        if (self.number > 0):
            ret += str(self.number) + "]"
        else:  # number = 0
            ret += " ]"

        return ret

    def display(self):
        print ("[" + str(self.number) + ": (" + str(self.positionx) + "," + str(self.positiony) + ")]")

    def distance(self):
        numberx = self.number % width
        numbery = self.number // width

        dist = ((self.positionx - numberx) * (self.positionx - numberx)) + (
                    (self.positionx - numbery) * (self.positionx - numbery))

        return dist


class Node:

    def __init__(self, state, sequence):
        self.state = state
        self.sequence = sequence

    def possiblemoves(self):
        boardtomove = Board(width, height)
        boardtomove.initialize(self.state)
        return boardtomove.possiblemoves()

    def makemove(self, move):
        boardtomove = Board(width, height)
        boardtomove.initialize(self.state)
        # boardtomove.display()
        # print ("next move :"+move)
        boardtomove.makemove(move)
        # boardtomove.display()
        return boardtomove


width = 4
height = 4
board = Board(width, height)
board.fillordered()
board.randomize(30)
# hard one, should be optimized :
# board.initialize("3-1-2-7-0-5-8-4-6-")

board.display()

# print "complexity " + str(board.complexity())
# print board.state()
start = Node(board.state(), "")
levels = []
currentlevel = [start]
nextlevel = []
visitedstates = [board.state()]

nearSolutionStates = {}
nearSolution = Node(board.state(), "")

if (board.state() == board.winstate()):
    exit("Already done, no resolution required")

iterations = 15
iteration = 0

for i in range(iterations):
    for node in currentlevel:
        for move in node.possiblemoves():
            if len(node.sequence) > 0 and node.sequence[-1] == opposite(move):
                continue  # no need to go back
            newsequence = []
            newsequence.extend(node.sequence)
            newsequence.append(move)
            movedboard = node.makemove(move)
            # sys.stdout.write('.')
            if movedboard.state() not in visitedstates:
                nodechild = Node(movedboard.state(), newsequence)
            nextlevel.append(nodechild)

    # evaluate if game is over
    newvisitedstate = False
    solutionfound = False

    for nd in nextlevel:
        brd = Board(width, height)
        brd.initialize(nd.state)

        if brd.state() == brd.winstate():
            print("we've got a winner")
            initial = Board(height, width)
            initial.initialize(start.state)
            initial.display()
            print(nd.sequence)
            brd.display()
            solutionfound = True
        else:
            if brd.state() not in visitedstates:
                visitedstates.append(brd.state())
                newvisitedstate = True

    if solutionfound == True:
        print("best solutions found exiting")
        exit()

    if newvisitedstate == False:
        print("no solution and no new states")
        exit()

    currentlevel = []
    currentlevel.extend(nextlevel)

    print("current level : " + str(iteration) + ", visited states : " + str(len(visitedstates)))
    # cmd = raw_input();
    # if cmd=='q':
    #    print ("user ends it")
    #    exit()
    # print "checked states : "+ str(len(visitedstates))

    iteration += 1
    if iteration > 100:
        exit("too long")