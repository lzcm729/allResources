# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 20:16:06 2020

@author: Qianzhen
"""
        

string = input()
strlen = len(string)
newString = string[0]
res = {}

wordDict = dict(zip(range(strlen), list(string)))

for gap in range(strlen):
    lastIndex = 0
    counterArray = [0]
    if gap == 0:
        counterArray = list(range(strlen))
    else:
        while len(counterArray) < strlen:               
            nextIndex = (lastIndex + gap + 1) % strlen
            if nextIndex in counterArray:
                nextIndex = nextIndex + 1
            counterArray = counterArray + [nextIndex]
            lastIndex = nextIndex
#    print(counterArray)
    newString = ''.join([wordDict[k] for k in counterArray])
    res[gap] = newString
#    print(newString)
        
                                            