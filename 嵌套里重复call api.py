# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 14:42:18 2019

@author: Nick
"""

a = ["无锡到广州", "广州到纽约"] #a是一个不停变换的值
judge = 0
res = 0

#方案一
while (1):
    input(a)
    if a == "无锡到广州":
        judge = 1
    if (judge == 1 and a == "广州到纽约"):
        res = 1
        break
    
#方案二
input(a)
if a == "无锡到广州":
    input(a)
    if a == "广州到纽约":
        res = 1
        
