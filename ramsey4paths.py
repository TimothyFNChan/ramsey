import numpy as np
import networkx as nx
from scipy.optimize import linprog
from collision import collision_matrix
from generate_patterns import generate_patterns
from gadgets import numPatterns
from colour_forcing import colour_forcing_sets
from branch import branch


numColors=3
omega=2
c=[0,1.0,2.0/3,2.0/4,2.0/5] #the conjectured bound for each k
numPatterns=numPatterns(omega,numColors)

# generate all principal patterns
patterns=generate_patterns(omega,numColors)
print(len(patterns))

# generate collision matrix
collisionMatrix=collision_matrix(patterns,numColors)
print collisionMatrix 

##CONSTRAINTS
objective=np.array([0]*numPatterns)
eqMatrix=np.array([[1]*numPatterns]) ##Constraint 4.6
eqVector=np.array([1])
ineqMatrix=np.empty((0,numPatterns))
ineqVector=np.array([])
#ineqVector will be generated later depending on how many lines of constraints we have in ineqMatrix


##Constraint 4.7
constraints47=np.empty((0,numPatterns)) #our set of constraints coming from ineq. 4.7
for i in range(numColors):
    for j in range(1,omega):
        for jprime in range(j+1,omega):
            newConstraint=[0]*numPatterns
            for index in range(numPatterns):
                pattern=patterns[index]
                if pattern[i][0]==j:
                    newConstraint[index]=-1
                elif pattern[i][0]==jprime:
                    newConstraint[index]=1
            newConstraint=np.array([newConstraint])
            constraints47=np.concatenate((constraints47,newConstraint),axis=0)
ineqMatrix=np.concatenate((ineqMatrix,constraints47),axis=0) #add these constraints to our big block
ineqVector=np.concatenate((ineqVector,np.zeros(np.shape(constraints47)[0])))

##Constraint 4.8
constraints48=np.empty((0,numPatterns))
for i in range(numColors):
    for j in range(1,omega):
        newConstraint=[0]*numPatterns
        for index in range(numPatterns):
            pattern=patterns[index]
            if pattern[i][0]==j:
                if pattern[i][1]==0:
                    newConstraint[index]=-1
                elif pattern[i][1]==1:
                    newConstraint[index]=1
        newConstraint=np.array([newConstraint])
        constraints48=np.concatenate((constraints48,newConstraint),axis=0)
ineqMatrix=np.concatenate((ineqMatrix,constraints48),axis=0)
ineqVector=np.concatenate((ineqVector,np.zeros(np.shape(constraints48)[0])))

##Constraint 4.9
constraints49=np.empty((0,numPatterns))
for i in range(numColors):
    for j in range(1,omega):
        newConstraint=[0]*numPatterns
        for index in range(numPatterns):
            pattern=patterns[index]
            if pattern[i][0]==j:
                if pattern[i][1]==0.5:
                    newConstraint[index]=1
                elif pattern[i][1]==1:
                    newConstraint[index]=2
        newConstraint=np.array([newConstraint])
        constraints49=np.concatenate((constraints49,newConstraint),axis=0)
ineqMatrix=np.concatenate((ineqMatrix,constraints49),axis=0)
ineqVector=np.concatenate((ineqVector,[c[numColors]]*np.shape(constraints49)[0]))

##Constraint 4.12

colour_forcing_sets(patterns,0,1,numColors)

#Search for a feasible solution to an optimisation problem
#minimise: objective^T * x subject to:  ineqMatrix_ub * x <= ineqVector, eqMatrix * x == eqVector

nsteps=100

conf=np.zeros((numPatterns),dtype=int)
iscontr=False
vxseq=np.array([],dtype=int)
onoffseq=np.array([],dtype=int)

##for step in range(nsteps):
##    brancheqMatrix=np.copy(eqMatrix)
##    brancheqVector=np.copy(eqVector)
##    for index in range(numPatterns):
##        if conf[index]==2:
##            newConstraint=np.zeros(numPatterns)
##            newConstraint[index]=1
##            brancheqMatrix=np.concatenate((brancheqMatrix,np.array([newConstraint])),axis=0)
##            brancheqVector=np.concatenate((brancheqVector,[0]))
##    branchProg=linprog(objective, ineqMatrix, ineqVector, brancheqMatrix, brancheqVector, bounds=(0,1))
##    if branchProg.status==2:
##        iscontradiction=True
##    else:
##        iscontradiction=False
##    [conf,vxseq,onoffseq]=branch(collisionMatrix,conf,vxseq,onoffseq,iscontradiction)
##    if not len(conf):
##        break
