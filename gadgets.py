# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:16:59 2018

@author: Yani
"""

#Because using 0,1,2 is easier than 0,0.5,1 for the values of vertices in each vertex cover

def indexToCover(n):
    if n==0:
        return 0.0
    if n==1:
        return 1.0/2
    if n==2:
        return 1.0
def coverToIndex(n):
    if n==0.0:
        return 0
    if n==0.5:
        return 1
    if n==1.0:
        return 2
    
def singleColorNum(omega):
    return 3*omega-2

def numPatterns(omega,numColors):
    return (3*omega-2)**numColors

def patternToIndex(pattern,numColors,omega):
    #given a pattern, find its index in our list without using the .find function
    index=0
    for color in range(numColors):
        component,coverValue=pattern[color][0],pattern[color][1]
        index=index+(3*(component-1)+ coverToIndex(coverValue)) * singleColorNum(omega) **(numColors-1-color)
    return index