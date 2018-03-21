import numpy as np
from scipy.optimize import linprog
numColors=4
omega=2

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
collisionMatrix=np.empty((numPatterns,numPatterns))
for i in range(numPatterns):
    for j in range(i,numPatterns):
        if collides(patterns[i],patterns[j]):
            collisionMatrix[i][j]=1
        else:
            collisionMatrix[i][j]=0
#symmetrise the adjacency matrix
print collisionMatrix
collisionMatrix=collisionMatrix+collisionMatrix.T - np.diag(collisionMatrix.diagonal())
        

##CONSTRAINTS
objective=np.array([0]*numPatterns)
eqMatrix=np.array([[1]*numPatterns])
eqVector=np.array([1])
ineqMatrix=np.empty((0,numPatterns))
#ineqVector will be generated later depending on how many lines of constraints we have in ineqMatrix


##Constraint 4.6
constraints46=np.empty((0,numPatterns)) #our set of constraints coming from ineq. 4.6
for i in range(numColors):
    for j in range(1,omega):
        for jprime in range(j+1,omega):
            newConstraint=[0]*numPatterns
            for index in range(numPatterns):
                pattern=patterns[index]
                if pattern[i][0]==j:
                    newConstraint[i]=-1
                elif pattern[i][0]==jprime:
                    newConstraint[i]=1
            newConstraint=np.array([newConstraint])
            constraints46=np.concatenate((constraints46,newConstraint),axis=0)
ineqMatrix=np.concatenate((ineqMatrix,constraints46),axis=0) #add these constraints to our big block


ineqVector=np.array([0]*ineqMatrix.shape[0])

#Search for a feasible solution to an optimisation problem
a=linprog(objective, ineqMatrix, ineqVector, eqMatrix, eqVector, bounds=(0,1))
