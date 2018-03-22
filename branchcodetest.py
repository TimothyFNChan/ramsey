# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:01:08 2018

@author: Yani
"""
import numpy as np
from branch import branch
import random 

testmatrix=np.array([[0,1,0,0,1,0,0,0,1],[1,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,1,0],[1,0,1,0,0,1,0,1,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,1,1,0,1,0,0],[1,0,0,0,0,0,0,0,0]])       
testconf=np.array([2,0,2,0,1,2,0,2,0])
testonoffseq=np.array([1])
testvxseq=np.array([4])

testansseq=[False,False,True,False,False,False,True,False,True,False] 


#generate random answers to iscontradiction to see behaviour

nsteps=10

conf=np.zeros((9),dtype=int)
iscontr=False
vxseq=np.array([],dtype=int)
onoffseq=np.array([],dtype=int)

for step in range(nsteps):
    [conf,vxseq,onoffseq]=branch(testmatrix,conf,vxseq,onoffseq,bool(random.getrandbits(1)))
    if not len(conf):
        break