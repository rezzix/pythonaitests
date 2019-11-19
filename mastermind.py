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
                print "in place"
                continue
            
            if guess[valx] in self.code :
                eval.existing += 1
                continue
        return eval
    def display(self):
        print (self.code)


class Evaluation:
    def __init__(self):
        self.inplace = 0
        self.existing = 0
    
    def display(self):
        print ("Inplace : {}, Existing : {}".format(self.inplace, self.existing))

#secretcode = Code({colors[randrange(0, 6)],colors[randrange(0, 6)],colors[randrange(0, 6)],colors[randrange(0, 6)]]})
secretcode = Code(['red', 'yellow', 'orange', 'orange'])

secretcode.display()

#secretcode.evaluate(['red', 'orange', 'blue', 'yellow']).display()
for indx in range(10) :
    guess = Code([])
    guess.randomize(4,colors)
    secretcode.evaluate(guess).display()
