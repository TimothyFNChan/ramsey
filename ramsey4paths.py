import numpy as np
from scipy.optimize import linprog
numColors=2 #must be at least 2
omega=2 #must be at least 2
c=[0,1.0,2.0/3,2.0/4,2.0/5] #the conjectured bound for each k

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

#generate the list of principal patterns according to modulo arithmetic
#starting from component 1, value 0 in every component, it varies later colours before earlier ones
#it also prefers varying cover value before component number
#May be better written recursively
#IF YOU DON't UNDERSTAND THIS:
#it's basically a generalisation of producing all {0,1}-valued sequences of length k
#by taking the digits of the binary representation of i for each i from 1 to 2^k
singleColorNum=(3*omega-2)
numPatterns=(3*omega-2)**numColors
patterns=[]
for i in range(numPatterns):
    pattern=[]
    colorRem=i
    for j in range(numColors-1,-1,-1):
        colorQuo,colorRem=divmod(colorRem,singleColorNum**j)
##        if colorQuo==singleColorNum-1:
##         pattern.append([omega]) #maybe [omega,0.0] would be better; to implement, remove this if statement
##        else:
        componentQuo,componentRem=divmod(colorQuo,3)
        pattern.append([componentQuo+1,indexToCover(componentRem)])
    patterns.append(pattern)

print(len(patterns))

#given a pattern, find its index in our list without using the .find function
def patternToIndex(pattern):
    index=0
    for color in range(numColors):
        component,coverValue=pattern[color][0],pattern[color][1]
        index=index+(3*(component-1)+ coverToIndex(coverValue)) * singleColorNum **(numColors-1-color)
    return index

###may be useful for generation
##import string
##digs = string.digits + string.ascii_letters
##
##
##def int2base(x, base):
##    if x < 0:
##        sign = -1
##    elif x == 0:
##        return digs[0]
##    else:
##        sign = 1
##
##    x *= sign
##    digits = []
##
##    while x:
##        digits.append(digs[int(x % base)])
##        x = int(x / base)
##
##    if sign < 0:
##        digits.append('-')
##
##    digits.reverse()
##
##    return ''.join(digits)

##Adjacency matrix for the collision graph
def collides(pattern1,pattern2):
    for k in range(numColors):
        pattern1Comp,pattern1Value=pattern1[k]
        pattern2Comp,pattern2Value=pattern2[k]
        if (pattern1Comp==pattern2Comp) and (pattern1Value+pattern2Value>=1):
            return 0
    return 1
collisionMatrix=np.zeros((numPatterns,numPatterns),dtype=int)
for i in range(numPatterns):
    for j in range(i,numPatterns):
        if collides(patterns[i],patterns[j]):
            collisionMatrix[i][j]=1
        else:
            collisionMatrix[i][j]=0
#symmetrise the adjacency matrix
collisionMatrix=np.copy(collisionMatrix+collisionMatrix.T - np.diag(collisionMatrix.diagonal()))
print collisionMatrix 

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

##Constraint 4.12
import networkx as nx
def isforcing(pattern1,pattern2,color):
    # input: 
    #       two patterns
    #       colour (int between 0 and numColors-1)
    # output:
    #       True if patterns force colour AND don't collide
    #       False if patterns collide OR don't force colour
    
    for k in range(color)+range(color+1,numColors): # numColors undefined!!!
        pattern1Comp,pattern1Value=pattern1[k]
        pattern2Comp,pattern2Value=pattern2[k]
        if (pattern1Comp==pattern2Comp) and (pattern1Value+pattern2Value>=1):
            return 0
    pattern1Comp,pattern1Value=pattern1[color]
    pattern2Comp,pattern2Value=pattern2[color]
    if (pattern1Comp==pattern2Comp) and (pattern1Value+pattern2Value>=1):
        return 1
    
    return 0
    
def colour_forcing_sets(patterns, colour,fraction):
    # input: 
    #       list of patterns
    #       colour
    #       fraction: will return maximal cliques of size at least fraction*cliquenumber
    #                 e.g. if fraction=0 returns all maximal cliques
    #                 if fraction=1 returns only maximum cliques
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
            if isforcing(patterns[i],patterns[j],colour):
                edgelist.append((i,j))
    
    G=nx.Graph()
    G.add_edges_from(edgelist)
    
    # draw graph G
    # nx.draw_networkx(G)
    
    cliqueslist=list(nx.find_cliques(G))
    cliquenumber=nx.graph_clique_number(G,cliqueslist)
    
    trimmedcliqueslist=filter(lambda x: len(x)>=cliquenumber*fraction,cliqueslist)
            
    # find maximal cliques
    return trimmedcliqueslist

maximalCliques=[]
for k in range(numColors):
    maximalCliques.append(colour_forcing_sets(patterns,k,1))

constraints412=np.empty((0,numPatterns))
for k in range(numColors):
    newConstraintBase=np.zeros(numPatterns,dtype=int)
    for index in range(numPatterns):
        pattern=patterns[index]
        if pattern[k][0]==1:
            newConstraintBase[index]=-1          
    for maximalClique in maximalCliques[k]:
        newConstraint=np.copy(newConstraintBase)
        for index in maximalClique:
            newConstraint[index]=newConstraint[index]+1
        newConstraint=np.array([newConstraint])
        constraints412=np.concatenate((constraints412,newConstraint),axis=0)
#ineqMatrix=np.concatenate((ineqMatrix,constraints412),axis=0)
#ineqVector=np.concatenate((ineqVector,np.zeros(np.shape(constraints412)[0])))

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

from branch import branch

nsteps=1000

conf=np.zeros((numPatterns),dtype=int)
iscontr=False
vxseq=np.array([],dtype=int)
onoffseq=np.array([],dtype=int)

#minimise: objective^T * x subject to:  ineqMatrix_ub * x <= ineqVector, eqMatrix * x == eqVector

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
    #I have specified the interior-point method, this may not be optimal
    branchProg=linprog(objective, ineqMatrix, ineqVector, brancheqMatrix, brancheqVector, bounds=(0,1),method='interior-point')

    binding=[]
    for i in range(numIneqConstraints):
        if branchProg.slack[i]<=0:
            binding.append(i)
    if branchProg.status==2:
        print 'Problem seems infeasible'
        iscontradiction=True
    elif branchProg.status==0:
        print 'The maximum epsilon is ' + str(-branchProg.fun)
        print 'The involved inequality constraints are ' +str(binding)
        if branchProg.fun>=-1.0e-8:
            iscontradiction=True
        else:
            iscontradiction=False
    else:
        print 'Unexpected branchProg.status' 
    [conf,vxseq,onoffseq]=branch(collisionMatrix,conf,vxseq,onoffseq,iscontradiction)
    if not len(conf):
        break
