# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:01:08 2018

@author: Yani
"""
import numpy as np
from branch import branch

collisionMatrix=np.load('collisionmatrix4paths.npy')

testansseq=np.array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1.,
       0., 1., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0.,
       1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1., 0.,
       1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 1.,
       0., 1., 0., 1., 0., 0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 1.,
       1., 0., 0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 1.])
testansseq=testansseq.astype(bool)

#generate random answers to iscontradiction to see behaviour

nsteps=100

conf=np.zeros((256),dtype=int)
iscontr=False
vxseq=np.array([],dtype=int)
onoffseq=np.array([],dtype=int)

for step in range(nsteps):
    [conf,vxseq,onoffseq]=branch(collisionMatrix,conf,vxseq,onoffseq,testansseq[step])
    if not len(conf):
        break