#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 00:01:17 2018

@author: ossama
"""
import sys
import levels

level = levels.l137

directions = ('e', 'w', 'n', 's')
iterations = 50000000
iteration = 0


class Board:
    def __init__(self):
        self.squares = [[]]
        self.reachablesquares = []

    def load(self, stringlevel):
        x = 0
        y = 0
        sqr = None
        # positionx, positiony, iswall, isgoal, hasbox, hasagent
        for i in level:
            if i not in [" ", "#", ".", "$", "+", "@", "*", "\n"]:
                continue
            if i == "\n":
                y += 1
                x = 0
                self.squares.append([])
                continue
            if i == " ":
                sqr = Square(self, x, y, False, False, False, False)
            if i == "#":
                sqr = Square(self, x, y, True, False, False, False)
            if i == ".":
                sqr = Square(self, x, y, False, True, False, False)
            if i == "$":
                sqr = Square(self, x, y, False, False, True, False)
            if i == "@":
                sqr = Square(self, x, y, False, False, False, True)
            if i == "+":
                sqr = Square(self, x, y, False, True, False, True)
            if i == "*":
                sqr = Square(self, x, y, False, True, True, False)
            x += 1
            self.squares[y].append(sqr)

    def display(self):
        disp = ""
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i])):
                disp += self.squares[i][j].toString()

            disp += "\n"

        print(disp)

    def displayreach(self):
        disp = ""
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i])):
                if self.squares[i][j] in self.agentreach():
                    disp += "@"
                else:
                    disp += self.squares[i][j].toString()

            disp += "\n"

        print(disp)

    def state(self):
        return self.boxpositionstr() + "|" + self.agentreachstr()

    def iswinstate(self):
        win = True
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i])):
                if self.squares[i][j].isgoal and not self.squares[i][j].hasbox:
                    win = False
                    break
            if win == False:
                break
        return win

    def boxpositions(self):
        ret = []
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i])):
                if self.squares[i][j].hasbox:
                    ret.append((i, j))
        return ret

    def boxpositionstr(self):
        ret = ""
        for pos in self.boxpositions():
            ret += '(' + str(pos[0]) + ',' + str(pos[1]) + ')'
        return ret

    def possiblemoves(self):
        possiblepushes = []
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i])):
                sqr = self.squares[i][j]
                if (sqr.hasbox):
                    for push in directions:
                        if (self.movedestination(sqr, push).isavailable()):
                            if (self.agentpositionbeforemove(sqr, push) in self.agentreach()):
                                if (not self.deadlock(sqr, push)):
                                    possiblepushes.append(Move(self.agentposition(), sqr, push))
        # pmstr =  "possible moves : "
        # for p in possiblepushes:
        #    pmstr = pmstr + "   " + p.toString()
        # print pmstr
        return possiblepushes

    def movedestination(self, square, direction):
        destination = None
        if (direction == "e"):
            destination = self.squares[square.positiony][square.positionx + 1]
        if (direction == "w"):
            destination = self.squares[square.positiony][square.positionx - 1]
        if (direction == "n"):
            destination = self.squares[square.positiony - 1][square.positionx]
        if (direction == "s"):
            destination = self.squares[square.positiony + 1][square.positionx]

        return destination

    # the position that the agent has before the move, if not possible returns None
    def agentpositionbeforemove(self, square, move):
        source = None
        if (move == "e"):
            source = self.squares[square.positiony][square.positionx - 1]
        if (move == "w"):
            source = self.squares[square.positiony][square.positionx + 1]
        if (move == "n"):
            source = self.squares[square.positiony + 1][square.positionx]
        if (move == "s"):
            source = self.squares[square.positiony - 1][square.positionx]

        if (source.isavailable()):
            return source
        else:
            return False

    # evaluates moves that lead to impossible to resolve boards
    def deadlock(self, square, push):
        if self.movedestination(square, push).iswallcorner() and not self.movedestination(square, push).isgoal:
            return True
        else:
            return False

    def agentposition(self):
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i])):
                if self.squares[i][j].hasagent:
                    return self.squares[i][j]

    def agentreach(self):
        if len(self.reachablesquares) > 0:
            return self.reachablesquares
        self.reachablesquares.append(self.agentposition())
        newreachablesquares = []
        while True:
            for square in self.reachablesquares:
                for move in directions:
                    destination = self.movedestination(square, move)
                    if destination.isavailable():
                        if destination not in self.reachablesquares and destination not in newreachablesquares:
                            newreachablesquares.append(destination)
            if len(newreachablesquares) > 0:
                for sqr in newreachablesquares:
                    self.reachablesquares.append(sqr)
                newreachablesquares = []
                continue
            else:
                break
        self.reachablesquares.sort(key=ordre)
        return self.reachablesquares

    def agentreachstr(self):
        ret = ""
        for pos in self.agentreach():
            ret += '(' + str(pos.positionx) + ',' + str(pos.positiony) + ')'
        return ret

    # takes possible moves, not protected against bad moves
    def makemove(self, move):
        if stepbystep:
            move.display()
        # self.display()
        # cmd = input()
        # if cmd == "r":
        #    self.displayreach()
        #    cmd = input()
        if stepbystep:
            s = stepbystep
        self.squares[move.sqragent.positiony][move.sqragent.positionx].hasagent = False
        # move.sqragent.hasagent = False
        self.squares[move.sqrbox.positiony][move.sqrbox.positionx].hasagent = True
        # move.sqrbox.hasagent = True
        self.squares[move.sqrbox.positiony][move.sqrbox.positionx].hasbox = False
        # move.sqrbox.hasbox = False
        self.movedestination(move.sqrbox, move.push).hasbox = True
        self.reachablesquares = []
        # self.display()
        return self

    def reversemove(self, move):
        # print "reverse move"
        # board.display()
        move.sqragent.hasagent = True
        move.sqrbox.hasagent = False
        move.sqrbox.hasbox = True
        self.movedestination(move.sqrbox, move.push).hasbox = False
        self.reachablesquares = []
        # board.display()
        return self

    def complexity(self):
        cmplx = 0
        for sqr in self.squares:
            cmplx += sqr.distance()
        return cmplx


class Square:

    def __init__(self, brd, positionx, positiony, iswall, isgoal, hasbox, hasagent):
        self.board = brd
        self.positionx = positionx
        self.positiony = positiony
        self.iswall = iswall
        self.isgoal = isgoal
        self.hasbox = hasbox
        self.hasagent = hasagent

    def toString(self):
        if (self.iswall):
            return "#"
        if (self.isgoal and self.hasbox):
            return "*"
        if (self.isgoal and self.hasagent):
            return "+"
        if (self.isgoal):
            return "."
        if (self.hasbox):
            return "$"
        if (self.hasagent):
            return "@"
        else:
            return " "

    def toStringPos(self):
        return "[" + self.toString() + ": (" + str(self.positionx) + "," + str(self.positiony) + ")]"

    def distance(self):
        return 0

    def isavailable(self):
        if self.iswall or self.hasbox:
            return False
        else:
            return True

    def iswallcorner(self):
        neighbourwalls = 0
        for sqr in self.neighbours().values():
            if sqr.iswall:
                neighbourwalls += 1
        if neighbourwalls >= 2:
            return True
        else:
            return False

    def neighbours(self):
        nghbr = {}
        if (len(self.board.squares) > self.positiony and len(self.board.squares[self.positiony + 1]) >= self.positionx):
            nghbr['s'] = self.board.squares[self.positiony + 1][self.positionx]
        if (self.positiony > 0):
            nghbr['n'] = self.board.squares[self.positiony - 1][self.positionx]
        if (self.positionx <= len(self.board.squares[self.positiony])):
            nghbr['e'] = self.board.squares[self.positiony][self.positionx + 1]
        if (self.positionx > 0):
            nghbr['w'] = self.board.squares[self.positiony][self.positionx - 1]
        return nghbr


# any significant order
def ordre(sqr):
    return sqr.positionx + sqr.positiony * 100


def runwinnerseq(sequence):
    b = Board()
    b.load(level)
    step = 1
    for mv in sequence:
        b.display()
        print("press enter to advance to step " + str(step) + "(or r to display agent reach):")
        step += 1
        cmd = input()
        if cmd == "r":
            b.displayreach()
            cmd = input()
        b.makemove(mv)
    b.display()

    print("problem solved")


class Move:
    def __init__(self, sqragent, sqrbox, push):
        self.sqragent = sqragent
        self.sqrbox = sqrbox
        self.push = push

    def display(self):
        print(self.sqrbox.toStringPos() + "move to : " + self.push)

    def toString(self):
        return self.sqrbox.toStringPos() + " move to " + self.push


class Node:

    def __init__(self, parent, brd, sequence):
        self.parent = parent
        self.board = brd
        self.sequence = sequence
        self.tried = False
        self.children = []

    def spawnchildren(self):
        for move in self.board.possiblemoves():
            childsequence = []
            childsequence.extend(self.sequence)
            childnode = Node(self, self.board, childsequence)
            childnode.sequence.append(move)
            self.children.append(childnode)

    def findsolution(self):
        global iteration
        iteration = iteration + 1
        if iteration > iterations:
            return ("too long")
        # print "finding solution iteration " + str (iteration) + " visited states : "+ str (len (visitedstates))

        self.board.makemove(self.sequence[-1])
        if self.board.state() in visitedstates:
            self.board.reversemove(self.sequence[-1])
            return
        if self.board.iswinstate():
            seqstr = ""
            for mv in self.sequence:
                seqstr += mv.toString() + "   "
            print ("found a winner with " + str(len(self.sequence)) + " " + seqstr)
            winnersequence.append(self.sequence)
        else:
            visitedstates.append(self.board.state())
            self.spawnchildren()
            for node in self.children:
                node.findsolution()

        self.board.reversemove(self.sequence[-1])


myboard = Board()
myboard.load(level)

myboard.display()

winnersequence = []

start = Node(None, myboard, [])
start.state = myboard.state()

visitedstates = [myboard.state()]

stepbystep = False

if (myboard.iswinstate()):
    exit("Already done, no resolution required")

start.spawnchildren()
for node in start.children:
    node.findsolution()

if len(winnersequence) > 0:
    winnersequence.sort(key=len)
    stepbystep = True
    print("best solution within " + str(len(winnersequence)) + " in " + str(iterations) + " iterations with " + str(len(winnersequence[0])) + " moves")

    runwinnerseq(winnersequence[0])
else:
    print("no solution found after " + str(iterations) + " iterations")