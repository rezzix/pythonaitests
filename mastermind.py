#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 00:01:17 2018

@author: ossama
"""

import sys
from random import randrange

colors = ('red', 'blue', 'green', 'yellow' ,'orange' ,'purple')

class Code:
    def __init__(self, values=None):
        self.code = []
        if (values is None) :
            for indx in range(4):
                self.code.append(colors[randrange(0, len(colors))])
            return
        for indx in range(len(values)):
            self.code.append(values[indx])
        
    def evaluate(self, guess):
        eval = Evaluation()
        for valx in range(len(guess)):
            #print ("{} gess {} code {}".format(valx, guess[valx], self.code[valx]))
            if  guess[valx] == self.code[valx] :
                eval.inplace += 1
                continue
            
            if guess[valx] in self.code :
                eval.existing += 1
                continue
        return eval
    def display(self):
        print (self.code)
    def equals(self, othercode):
        for indx in range(len(self.code)) :
            if self.code[indx] != othercode.code[indx]:
                return False
        return True


class Evaluation:
    def __init__(self):
        self.inplace = 0
        self.existing = 0

    def perfect(self) :
        if self.inplace == 4 :
            return True
        else :
            return False

    def equals(self, otherevaluation):
        if (self.inplace==otherevaluation.inplace and self.existing==otherevaluation.existing):
            return True
        else:
            return False    
    def display(self):
        print ("Inplace : {}, Existing : {}".format(self.inplace, self.existing))

class Solver:
    def displaySolution(self):
        if self.solution is not None:
            print("perfect code using {} guesses and skipping {} : {}".format(self.usedguesses, self.skippedguesses, self.solution.code))
        else:
            print("not found using {} guesses and skipping {}".format(self.usedguesses, self.skippedguesses))
# Stupid solver only uses memory, it will not give the guess twice
class StupidSolver(Solver):
    def solve(self, code):
        guesses = []
        evaluations = []
        eval = Evaluation()

        while not eval.perfect() :
            guess = Code()
            if any(guess.equals(g) for g in guesses):
                continue
            guesses.append(guess)
            if len(guesses)==6**4:
                break
            eval = code.evaluate(guess.code)
            evaluations.append(eval)

        self.solution = guesses[len(guesses)-1]
        self.usedguesses = len(guesses)
        self.skippedguesses = 0

# Verifier solver will check against available results before making a guess
class VerifierSolver(Solver):
    def solve(self, code, firstguess=None):
        guesses = []
        badguesses = []
        evaluations = []
        eval = Evaluation()
        nextguess = firstguess

        while len(guesses) + len(badguesses) <= 6**4 and not eval.perfect() :
            guess = nextguess if nextguess is not None else Code()
            nextguess = None
            if any(guess.equals(g) for g in guesses):
                continue
            if any(guess.equals(g) for g in badguesses):
                continue
            # good guess based on history
            goodguess = True
            for indx in range(len(guesses)):
                if not guess.evaluate(guesses[indx].code).equals(evaluations[indx]):
                    goodguess = False
                    break
            if not goodguess :
                badguesses.append(guess)
                continue
            guesses.append(guess)
            eval = code.evaluate(guess.code)
            evaluations.append(eval)
        self.solution = guesses[len(guesses)-1]
        self.usedguesses = len(guesses)
        self.skippedguesses = len(badguesses)

secretcode = Code()
secretcode.display()

print('\nStupid solver processing : \n')
solver1 = StupidSolver()
solver1.solve(secretcode)
solver1.displaySolution()

print('\nVerifier solver processing : \n')
solver2 = VerifierSolver()
solver2.solve(secretcode,Code(["red","red","orange","orange"]))
solver2.displaySolution()
