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
            self.code[indx] = values[indx] 
    def evaluate(self, guess):
        eval = Evaluation(0,0)
        for valx in guess
            inplace = false
            if ( guess[valx] == self.code[valx] )
                eval.inplace += 1
                inplace = true
                continue
            
            if (guess[indx] in self.code)
                eval.existing += 1
                continue
        return eval
    def display(self):
        print self.code


class Evaluation:
    def __init__(self, inplace, existing):
        self.inplace = inplace
        self.existing = existing
    
    def display(self):
        print "Inplace : " + self.inplace + " , Existing : " + self.existing

#secretcode = Code({colors[randrange(0, 6)],colors[randrange(0, 6)],colors[randrange(0, 6)],colors[randrange(0, 6)]]})
secretcode = Code({"red","yellow","orange","orange"})

secretcode.display()

secretcode.eval({'red', 'blue', 'green', 'yellow'}).display()
