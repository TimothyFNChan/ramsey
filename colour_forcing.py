# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:35:14 2018

@author: Yani
"""

import networkx as nx
import random as rand
import numpy as np

def isforcing(pattern1,pattern2,color,numColors):
    # input: 
    #       two patterns
    #       colour (int between 0 and numColors-1)
    #       number of colors in ramsey problem
    # output:
    #       True if patterns force colour AND don't collide
    #       False if patterns collide OR don't force colour
    
    for k in range(color)+range(color+1,numColors): # numColors undefined!!!
        pattern1Comp,pattern1Value=pattern1[k]
        pattern2Comp,pattern2Value=pattern2[k]
        if (pattern1Comp==pattern2Comp) and (pattern1Value+pattern2Value>=1):
            return 0
    #simple version that matches the definition given in the paper
    #MAKE SURE THIS IS COMMENTED IF YOU WANT TO SAVE TIME
    #return 1

    #complex version that does not add edges between colliding vertices to save time
    pattern1Comp,pattern1Value=pattern1[color]
    pattern2Comp,pattern2Value=pattern2[color]
    if (pattern1Comp==pattern2Comp) and (pattern1Value+pattern2Value>=1):
        return 1
    return 0


    
def colour_forcing_sets(patterns, colour,fraction,numColors,outputfile):
    # input: 
    #       list of patterns
    #       colour
    #       fraction: will return maximal cliques of size at least fraction*cliquenumber
    #                 e.g. if fraction=0 returns all maximal cliques
    #                 if fraction=1 returns only maximum cliques
    #       numColors = number of colors in ramsey problem
    #       outputfile = write all output there
    # output:
    #       list of maximal sets of patterns such that any two force the colour
    #       list is of the form [l_1,l_2,...] where l_i is a list of indices 
    #       of array "patterns" any two of which force the colour
    
    # WARNING: Might have high-ish space complexity!
    
    # Generate graph of forcing pattern pairs
    npatterns=len(patterns)
    edgelist=[]
    for i in range(npatterns):
        for j in range(i,npatterns):
            if isforcing(patterns[i],patterns[j],colour,numColors):
                edgelist.append((i,j))
    
    G=nx.Graph()
    G.add_edges_from(edgelist)
    
    # draw graph G
    # nx.draw_networkx(G)
    
    cliqueslist=list(nx.find_cliques(G))
    cliquenumber=nx.graph_clique_number(G,cliqueslist)
    
    trimmedcliqueslist=filter(lambda x: len(x)>=cliquenumber*fraction,cliqueslist)
            
    # find maximal cliques
    print 'There will be '+str(len(trimmedcliqueslist))+' 4.12 constraints for colour '+str(colour)  
    outputfile.write('There will be '+str(len(trimmedcliqueslist))+' 4.12 constraints for colour '+str(colour)  +'\n')
    return trimmedcliqueslist

def colour_forcing_sets_disjoint(patterns, colour, fraction,numColors,outputfile):
    # input: 
    #       list of patterns
    #       colour
    #       fraction: will return maximal cliques of size at least fraction*cliquenumber
    #                 e.g. if fraction=0 returns all maximal cliques
    #                 if fraction=1 returns only maximum cliques
    #       numColors = number of colors in ramsey problem
    #       outputfile = write all output there
    # output:
    #       list of maximal sets of patterns such that any two force the colour
    #       list is of the form [l_1,l_2,...] where l_i is a list of indices 
    #       of array "patterns" any two of which force the colour
    
    # Generate graph of forcing pattern pairs
    npatterns=len(patterns)
    edgelist=[]
    for i in range(npatterns):
        for j in range(i,npatterns):
            if isforcing(patterns[i],patterns[j],colour,numColors):
                edgelist.append((i,j))
    
    G=nx.Graph(edgelist)
    initialcliquenumber=nx.graph_clique_number(G)

    disjointcliqueslist=[]
    
    while nx.number_of_edges(G)>0:
        cliques=nx.find_cliques(G)
        cliquenumber=nx.graph_clique_number(G)
        if cliquenumber<fraction*initialcliquenumber:
            return disjointcliqueslist
        else:
            while True:
                currentclique=cliques.next()
                if len(currentclique)==cliquenumber:
                    break
            disjointcliqueslist.append(currentclique)
            vertices=G.nodes()
            G=G.subgraph([x for x in vertices if x not in currentclique])
    print 'There will be '+str(len(disjointcliqueslist))+' 4.12 constraints' 
    outputfile.write('There will be '+str(len(disjointcliqueslist))+' 4.12 constraints\n')
    return disjointcliqueslist
    
            
def colour_forcing_sets_random(patterns, colour, numCliques,numColors,outputfile):
    # input: 
    #       list of patterns
    #       colour
    #       numCliques = number of cliques that will be returned
    #       numColors = number of colors in ramsey problem
    #       outputfile = write all output there    
    # output:
    #       list of maximal sets of patterns such that any two force the colour
    #       list is of the form [l_1,l_2,...] where l_i is a list of indices 
    #       of array "patterns" any two of which force the colour
    
    
    # Generate graph of forcing pattern pairs
    npatterns=len(patterns)
    edgelist=[]
    for i in range(npatterns):
        for j in range(i,npatterns):
            if isforcing(patterns[i],patterns[j],colour,numColors):
                edgelist.append((i,j))
    
    G=nx.Graph(edgelist)
    cliqueslist=list(nx.find_cliques(G))
    
    cliqueslist=[cliqueslist[i] for i in rand.sample(xrange(len(cliqueslist)),min(numCliques,len(cliqueslist)))]
 
    print 'There will be '+str(len(cliqueslist))+' 4.12 constraints' 
    outputfile.write('There will be '+str(len(cliqueslist))+' 4.12 constraints\n' )
    return cliqueslist        
    
