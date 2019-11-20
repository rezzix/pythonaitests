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
    def __init__(self, values):
        self.code = []
        for indx in range(len(values)):
            self.code.append(values[indx])
    def randomize(self, length, choices):
        self.code=[]
        for indx in range(length):
            self.code.append(choices[randrange(0, len(choices))])
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


# Stupid solver only uses memory, it will not give the guess twice
class StupidSolver:
    def solve(self, code):
        guesses = []
        evaluations = []
        eval = Evaluation()

        while not eval.perfect() :
            guess = Code([])
            guess.randomize(4,colors)
            if any(guess.equals(g) for g in guesses):
                continue
            guesses.append(guess)
            if len(guesses)==6**4:
                break
            eval = code.evaluate(guess.code)
            evaluations.append(eval)

        if eval.perfect():
            print("perfect code using {} guesses".format(len(guesses)))
        else:
            print("not found using {} guesses".format(len(guesses)))
        guesses[len(guesses)-1].display() 

# Verifier solver will check against available results before making a guess
class VerifierSolver:
    def solve(self, code):
        guesses = []
        badguesses = []
        evaluations = []
        eval = Evaluation()

        while len(guesses) + len(badguesses) <= 6**4 and not eval.perfect() :
            guess = Code([])
            guess.randomize(4,colors)
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
            guess.display()
            eval.display()

        if eval.perfect():
            print("perfect code using {} guesses and skipping {}".format(len(guesses), len(badguesses)))
        else:
            print("not found using {} guesses and skipping {}".format(len(guesses), len(badguesses)))
        guesses[len(guesses)-1].display()     

#secretcode = Code({colors[randrange(0, 6)],colors[randrange(0, 6)],colors[randrange(0, 6)],colors[randrange(0, 6)]]})
secretcode = Code(['red', 'yellow', 'orange', 'orange'])
secretcode.display()

print('\nStupid solver processing : \n')
solver1 = StupidSolver()
solver1.solve(secretcode)

print('\nVerifier solver processing : \n')
solver2 = VerifierSolver()
solver2.solve(secretcode)

