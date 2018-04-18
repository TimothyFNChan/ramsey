# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:14:17 2018

@author: Yani
"""
from gadgets import numPatterns,singleColorNum,indexToCover

def generate_patterns(omega, numColors):
    # input: omega = looking at first omega connected components in each color
    #        numColors = number of colors for given ramsey problem
    # output: list of all patterns for given omega an numColors
    
    # DOC:
    # generate the list of principal patterns according to modulo arithmetic
    # starting from component 1, value 0 in every component, it varies later colours before earlier ones
    # it also prefers varying cover value before component number
    # May be better written recursively
    # IF YOU DON't UNDERSTAND THIS:
    # it's basically a generalisation of producing all {0,1}-valued sequences of length k
    # by taking the digits of the binary representation of i for each i from 1 to 2^k
    
    patterns=[]
    for i in range(numPatterns(omega, numColors)):
        pattern=[]
        colorRem=i
        for j in range(numColors-1,-1,-1):
            colorQuo,colorRem=divmod(colorRem,singleColorNum(omega)**j)
            componentQuo,componentRem=divmod(colorQuo,3)
            pattern.append([componentQuo+1,indexToCover(componentRem)])
        patterns.append(pattern)
    return patterns