import numpy as np
import networkx as nx
import sys
import simplejson
from scipy.optimize import linprog
from collision import collision_matrix
from generate_patterns import generate_patterns
from gadgets import numPatterns
from colour_forcing import colour_forcing_sets
from colour_forcing import colour_forcing_sets_disjoint
from colour_forcing import colour_forcing_sets_random
from branch import branch

#Confirmed working:
#2 colors
#2 colors, omega=2, strong deterministic cliqueFraction 0.8, minSize 0.74

numColors=3
omega=2
minComponentSize=[np.nan,np.nan,1,0.74,1.0/3]
cliquesMethod='deterministic' #'simple', 'deterministic', 'disjoint', or 'random'
cliqueFraction=0 #only relevant if cliquesMethod==deterministic or disjoint
numCliques=100 #only relevant if cliquesMethod==random

c=[0,1.0,2.0/3,2.0/4,2.0/5] #the conjectured bound for each k
numPatterns=numPatterns(omega,numColors)

# generate all principal patterns
patterns=generate_patterns(omega,numColors)
print 'There are ' + str(len(patterns)) + ' patterns.'

# generate collision matrix
collisionMatrix=collision_matrix(patterns,numColors)

##CONSTRAINTS
objective=np.array([0]*numPatterns,dtype=int)
eqMatrix=np.array([[1]*numPatterns],dtype=int) ##Constraint 4.6
eqVector=np.array([1])
ineqMatrix=np.empty((0,numPatterns),dtype=int)
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

####Constraint 4.12
def naturalForcing(pattern,k):
    for k2 in range(k)+range(k+1,numColors):
        if pattern[k2][0]==omega or pattern[k2][1]!=0:
            return False
    return True
if cliquesMethod=='deterministic' or cliquesMethod=='disjoint' or cliquesMethod=='random':
    maximalCliques=[]
    if cliquesMethod=='deterministic':
        for k in range(numColors):
            maximalCliques.append(colour_forcing_sets(patterns,k,cliqueFraction,numColors))
    elif cliquesMethod=='disjoint':
        for k in range(numColors):
            maximalCliques.append(colour_forcing_sets_disjoint(patterns,k,cliqueFraction,numColors))
    elif cliquesMethod=='random':
        for k in range(numColors):
            maximalCliques.append(colour_forcing_sets_random(patterns,k,numCliques,numColors))
            
    constraints412=np.empty((0,numPatterns))
    constr_file = open('constraint412.txt','w') 
    constr_file.write('[')
    for k in range(numColors):
        print '\nGenerating constraints 4.12 for colour '+str(k)
        total=len(maximalCliques[k])
        newConstraintBase=[0]*numPatterns
        for index in range(numPatterns):
            pattern=patterns[index]
            if pattern[k][0]==1:
                newConstraintBase[index]=-1          
        for i,maximalClique in enumerate(maximalCliques[k]):
            newConstraint=newConstraintBase[:]
            for index in maximalClique:
                newConstraint[index]=newConstraint[index]+1
            sys.stdout.write('\r'+str(i)+'/'+str(total))
            simplejson.dump(newConstraint,constr_file)
            if i!=len(maximalCliques[k])-1 or k!=numColors-1:
                constr_file.write(',')
    constr_file.write(']')
    constr_file.close()
    constr_file=open('constraint412.txt','r')
    constraints412=np.array(simplejson.load(constr_file))
    ineqMatrix=np.concatenate((ineqMatrix,constraints412),axis=0)
    ineqVector=np.concatenate((ineqVector,np.zeros(np.shape(constraints412)[0])))

    print '\nAll constraints 4.12 have been successfully generated'
        
    #Constraint 4.12 simplified
 
    constraints412=np.empty((0,numPatterns))
    for k in range(numColors):
        newConstraintBase=[0]*numPatterns
        for index in range(numPatterns):
            pattern=patterns[index]
            if pattern[k][0]==1:
                newConstraintBase[index]=-1
                print patterns[index]
        print newConstraintBase
        for index in range(numPatterns):
            pattern=patterns[index]
            if naturalForcing(pattern,k):
                newConstraintBase[index]=newConstraintBase[index]+1
                print patterns[index]
        print newConstraintBase
        newConstraint=np.array([newConstraintBase])
        constraints412=np.concatenate((constraints412,newConstraint),axis=0)
    ineqMatrix=np.concatenate((ineqMatrix,constraints412),axis=0)
    ineqVector=np.concatenate((ineqVector,np.zeros(np.shape(constraints412)[0])))
else:
    print 'Unexpected cliquesMethod'
    quit

####Constraint 4.13 (Minimum component size)
constraints413=np.empty((0,numPatterns))
newConstraint=[0]*numPatterns
for index in range(numPatterns):
    pattern=patterns[index]
    if pattern[0][0]==1:
        newConstraint[index]=-1
newConstraint=np.array([newConstraint])
constraints413=np.concatenate((constraints413,newConstraint),axis=0)

ineqMatrix=np.concatenate((ineqMatrix,constraints413),axis=0)
ineqVector=np.concatenate((ineqVector,[-minComponentSize[numColors]]))

##Constraint 4.9 (With the strictness constraint)
##This adds one more variable, epsilon, to our polytope
        
#Padding old constraints to fit the new matrix dimensions
objective=np.concatenate((objective,[-1])) #Minimise -epsilon i.e. Maximise epsilon
neweqCol=np.array([[0]*np.shape(eqMatrix)[0]]).T
eqMatrix=np.concatenate((eqMatrix,neweqCol),axis=1)
newineqCol=np.array([[0]*np.shape(ineqMatrix)[0]]).T
ineqMatrix=np.concatenate((ineqMatrix,newineqCol),axis=1)

constraints49=np.empty((0,numPatterns+1))
for i in range(numColors):
    for j in range(1,omega):
        newConstraint=[0]*(numPatterns+1)
        for index in range(numPatterns):
            pattern=patterns[index]
            if pattern[i][0]==j:
                if pattern[i][1]==0.5:
                    newConstraint[index]=1
                elif pattern[i][1]==1:
                    newConstraint[index]=2
        newConstraint[numPatterns]=1 #epsilon
        newConstraint=np.array([newConstraint])
        constraints49=np.concatenate((constraints49,newConstraint),axis=0)
ineqMatrix=np.concatenate((ineqMatrix,constraints49),axis=0)
ineqVector=np.concatenate((ineqVector,[c[numColors]]*np.shape(constraints49)[0]))


#Search for a feasible solution to an optimisation problem
#minimise: objective^T * x subject to:  ineqMatrix_ub * x <= ineqVector, eqMatrix * x == eqVector

nsteps=10000

conf=np.zeros((numPatterns),dtype=int)
iscontr=False
vxseq=np.array([],dtype=int)
onoffseq=np.array([],dtype=int)

numIneqConstraints=ineqMatrix.shape[0]
for step in range(nsteps):
    brancheqMatrix=np.copy(eqMatrix)
    brancheqVector=np.copy(eqVector)
    for index in range(numPatterns):
        if conf[index]==2:
            newConstraint=np.zeros(numPatterns+1) #+1 because of the epsilon
            newConstraint[index]=1
            brancheqMatrix=np.concatenate((brancheqMatrix,np.array([newConstraint])),axis=0)
            brancheqVector=np.concatenate((brancheqVector,[0]))
    #I have specified the interior-point method, this may not be optimal but it seems to behave better
    branchProg=linprog(objective, ineqMatrix, ineqVector, brancheqMatrix, brancheqVector, bounds=(0,1),method='interior-point')

    print ''
    binding=[]
    for i in range(numIneqConstraints):
        if branchProg.slack[i]<=1.0e-10:
            binding.append(i)
    if branchProg.status==2:
        print 'Problem seems infeasible'
        iscontradiction=True
    elif branchProg.status==0:
        print 'The maximum epsilon is ' + str(-branchProg.fun)
        print 'The involved inequality constraints are ' +str(binding)
        print 'The computed solution is ' + str(branchProg.x)
        if np.sum(branchProg.x[:12])<1:
            print 'Minimum component size flag (only for numColors=2)'
            print 'Expected: 0, got: ' + str(np.sum(branchProg.x[3]+branchProg.x[7]+branchProg.x[11]+branchProg.x[15]))
        if branchProg.fun>=-1.0e-8:
            iscontradiction=True
            print 'Solution failed the strictness conditions'
        else:
            iscontradiction=False
    else:
        print 'Unexpected branchProg.status'
        quit
    [conf,vxseq,onoffseq]=branch(collisionMatrix,conf,vxseq,onoffseq,iscontradiction)
    if not len(conf):
        break
