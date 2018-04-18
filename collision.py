# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 12:03:52 2018

@author: Yani
"""

import numpy as np

def collides(pattern1,pattern2,numColors):
    # input: two patterns
    #        numColors = number of colors in ramsey problem
    # output: 0 if patterns collide ???
    #         1 if patterns don't collide ???
    
    for k in range(numColors):
        pattern1Comp,pattern1Value=pattern1[k]
        pattern2Comp,pattern2Value=pattern2[k]
        if (pattern1Comp==pattern2Comp) and (pattern1Value+pattern2Value>=1):
            return 0
    return 1

def collision_matrix(patterns,numColors):
    # inpot: list of patterns
    #        numColors = number of colors in ramsey problem
    # output: collision matrix for this list of patterns
    #         entry i,j = 1 if i-th and j-th patterns collide
    #                     0 if i-th and j-th patterns don't collide
    
    numPatterns=len(patterns)
    collisionMatrix=np.zeros((numPatterns,numPatterns),dtype=int)
    for i in range(numPatterns):
        for j in range(i,numPatterns):
            if collides(patterns[i],patterns[j],numColors):
                collisionMatrix[i][j]=1
            else:
                collisionMatrix[i][j]=0
    #symmetrise the adjacency matrix
    return collisionMatrix+collisionMatrix.T - np.diag(collisionMatrix.diagonal())