# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:35:14 2018

@author: Yani
"""

import networkx as nx


def isforcing(pattern1,pattern2,color):
    # input: 
    #       two patterns
    #       colour (int between 0 and numColors-1)
    # output:
    #       True if patterns force colour AND don't collide
    #       False if patterns collide OR don't force colour
    
    for k in range(color)+range(color+1,numColors):
        pattern1Comp,pattern1Value=pattern1[k]
        pattern2Comp,pattern2Value=pattern2[k]
        if (pattern1Comp==pattern2Comp) and (pattern1Value+pattern2Value>=1):
            return 0
    pattern1Comp,pattern1Value=pattern1[colour]
    pattern2Comp,pattern2Value=pattern2[colour]
    if (pattern1Comp==pattern2Comp) and (pattern1Value+pattern2Value>=1):
        return 1
    
    return 0
    
def colour_forcing_sets(patterns, colour):
    # input: 
    #       list of patterns
    #       colour
    # output:
    #       list of maximal sets of patterns such that any two force the colour
    #       list is of the form [l_1,l_2,...] where l_i is a list of indices 
    #       of array "patterns" any two of which force the colour
    
    
    # Generate graph of forcing pattern pairs
    npatterns=len(patterns)
    edgelist=[]
    for i in range(npatterns):
        for j in range(i,npatterns):
            if isforcing(patterns[i],patterns[j],colour):
                edgelist.append((i,j))
    
    G=nx.Graph()
    G.add_edges_from(edgelist)
    
    # find maximal cliques
    return list(nx.find_cliques(G))
