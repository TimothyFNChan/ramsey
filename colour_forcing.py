# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:35:14 2018

@author: Yani
"""

import networkx as nx


def force_colour(pattern1,pattern2,colour):
    # input: 
    #       two patterns
    #       colour
    # output:
    #       True if patterns force colour
    #       False if patterns don't force colour
    
    # TIM CAN YOU WRITE THIS
    return False
    
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
            if force_colour(patterns[i],patterns[j],colour):
                edgelist.append((i,j))
    
    G=nx.Graph()
    G.add_edges_from(edgelist)
    
    # find maximal cliques
    return list(nx.find_cliques(G))