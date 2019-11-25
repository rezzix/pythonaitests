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
            
            if guess[valx] in self.code and guess[valx] != self.code[valx] :
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
    def __init__(self):
        self.guesses = []
        self.badguesses = []
        self.evaluations = []
        
    def displaySolution(self):
        if self.solution is not None:
            print("perfect code using {} guesses and skipping {} : {}".format(len(self.guesses), len(self.badguesses), self.solution.code))
        else:
            print("not found using {} guesses and skipping {}".format(len(self.guesses), len(self.badguesses)))
# Stupid solver only uses memory, it will not give the guess twice
class StupidSolver(Solver):
    def solve(self, code):
        eval = Evaluation()
        while not eval.perfect() :
            guess = Code()
            if any(guess.equals(g) for g in self.guesses):
                continue
            self.guesses.append(guess)
            if len(self.guesses)==6**4:
                break
            eval = code.evaluate(guess.code)
            self.evaluations.append(eval)

        self.solution = self.guesses[len(self.guesses)-1]

# Verifier solver will check against available results before making a guess
class VerifierSolver(Solver):
    def solve(self, code, firstguess=None):
        nextguess = firstguess
        eval = Evaluation()
        while len(self.guesses) + len(self.badguesses) <= 6**4 and not eval.perfect() :
            guess = nextguess if nextguess is not None else Code()
            nextguess = None
            if any(guess.equals(g) for g in self.guesses):
                continue
            if any(guess.equals(g) for g in self.badguesses):
                continue
            # good guess based on history
            goodguess = True
            for indx in range(len(self.guesses)):
                if not guess.evaluate(self.guesses[indx].code).equals(self.evaluations[indx]):
                    goodguess = False
                    break
            if not goodguess :
                self.badguesses.append(guess)
                continue
            self.guesses.append(guess)
            eval = code.evaluate(guess.code)
            self.evaluations.append(eval)
        self.solution = self.guesses[len(self.guesses)-1]
        self.usedguesses = len(self.guesses)
    def stepsolve(self, eval):
        if eval is None:
            guess = Code()
            self.guesses.append(guess) 
            return guess
        self.evaluations.append(eval)
        guess=None
        goodguess = False
        codestried = 0
        # fixme add condition to break if too much guesses, means that evaluations where wrong
        while not goodguess :
            guess=nextcode(guess)
            goodguess = True
            codestried +=1
            for indx in range(len(self.guesses)):
                if codestried>6**4 :
                    print("resolution impossible, there should be a mistake in evaluations")
                    quit()
                if not guess.evaluate(self.guesses[indx].code).equals(self.evaluations[indx]):
                    goodguess = False
                    break
            if not goodguess :
                self.badguesses.append(guess)
                continue
            else : 
                self.guesses.append(guess)
        return guess

def testResolvers(secretcode, xtimes):
    print('\nStupid solver processing {} times: \n'.format(xtimes))
    solver1guesses = []
    for i in range(xtimes):
        solver1 = StupidSolver()
        solver1.solve(secretcode)
        solver1guesses.append(len(solver1.guesses))

    print (" -> average in series of used guesses : {}".format(sum(solver1guesses)/len(solver1guesses)))

    print('\nVerifier solver processing with random init {} times: \n'.format(xtimes))
    solver2guesses = []
    for i in range(xtimes):
        solver2 = VerifierSolver()
        solver2.solve(secretcode)
        solver2guesses.append(len(solver2.guesses))

    print (" -> average in series of used guesses : {}".format((sum(solver2guesses)+0.0)/len(solver2guesses)))


    print('\nVerifier solver processing with 2 colors init {} times: \n'.format(xtimes))
    solver2guesses = []
    for i in range(xtimes):
        solver2 = VerifierSolver()
        solver2.solve(secretcode,Code(["red","red","orange","orange"]))
        solver2guesses.append(len(solver2.guesses))

    print (" -> average in series of used guesses : {}".format((sum(solver2guesses)+0.0)/len(solver2guesses)))

    print('\nVerifier solver processing with 3 colors init {} times: \n'.format(xtimes))
    solver2guesses = []
    for i in range(xtimes):
        solver2 = VerifierSolver()
        solver2.solve(secretcode,Code(["red","red","blue","orange"]))
        solver2guesses.append(len(solver2.guesses))

    print (" -> average in series of used guesses : {}".format((sum(solver2guesses)+0.0)/len(solver2guesses)))

    print('\nVerifier solver processing with 4 colors init {} times: \n'.format(xtimes))
    solver2guesses = []
    for i in range(xtimes):
        solver2 = VerifierSolver()
        solver2.solve(secretcode,Code(["red","green","blue","orange"]))
        solver2guesses.append(len(solver2.guesses))

    print (" -> average in series of used guesses : {}".format((sum(solver2guesses)+0.0)/len(solver2guesses)))

def nextcode(code):
    if code is None:
        return Code()
    if code.equals(Code([colors[-1],colors[-1],colors[-1],colors[-1]])):
        return Code([colors[0],colors[0],colors[0],colors[0]])
    ret=Code(code.code)
    for indx in range(len(ret.code)):
        if colors.index(ret.code[indx]) < (len(colors)-1):
            ret.code[indx] = colors[colors.index(ret.code[indx])+1]
            break
        else:
            ret.code[indx] = colors[0]
            continue
    return ret

def play():
    print ("write down your code exemple ['red','blue','orange','green']")
    print ("now you'll evaluate my guess")
    eval = None
    vs = VerifierSolver()

    while eval is None or not eval.perfect() :
        guess = vs.stepsolve(eval)
        guess.display()
        print ("guess : ")
        eval = Evaluation()
        while True:
            eval.inplace = input  ("-> in correct place (0 to 4)            ?  ")
            if eval.inplace>=0 and eval.inplace<=4 :
                break
        while True:    
            eval.existing = input ("-> existing but in wrong place (0 to 4) ?  ")
            if eval.existing>=0 and eval.existing<=4 :
                break
        
        if eval.perfect():
            print ('found it')
            break
    
        
        




secretcode = Code()
secretcode.display()

#solver = VerifierSolver()
#solver.solve(secretcode)
#solver.displaySolution()
play()

