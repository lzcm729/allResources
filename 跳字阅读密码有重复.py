# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 15:27:43 2020

@author: Qianzhen
"""

string = input()

strlen = len(string)
res = {}
#for gap in range(strlen):
#    resValue = []
#    if gap == 0:
#        resValue = string
#    else:
#        strlist = string * (gap+1)
#        calstr = ([1] + [0]*gap) * strlen
#        for signal in calstr:
#            if signal == 1:
#                resValue.append(strlist[calstr.index(signal)])
#                calstr[calstr.index(signal)] = 2
#        resValue = ''.join(resValue)
#        res[gap] = resValue
        
for gap in range(strlen):
    resValue = []
    strlist = string * (gap+1)
    calstr = ([1] + [0]*gap) * strlen
    for signal in calstr:
        if signal == 1:
            resValue.append(strlist[calstr.index(signal)])
            calstr[calstr.index(signal)] = 2
    resValue = ''.join(resValue)
    res[gap] = resValue