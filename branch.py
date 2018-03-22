import numpy as np

def branch(collisionMatrix, configuration, vertexsequence, onoffsequence, iscontradiction):
    # input: adjacency matrix of collision graph for patterns
    #       configuration = configuration of on/offs for all patterns that was just checked for contradiction
    #       vertexsequence = vertices whose turning on/off in sequence yielded the contradiction
    #       onoffsequence = on/off status corresponding to vertexsequence
    #       iscontradiction = result of linear programming check on corresponding constraints
    # output:
    #       list of three lists in this order:
    #       newconfiguration = to be tried next
    #       newvertexseqence = to be passed as vertexsequence to next instance of branch
    #       newonoffsequence = to be passed as onoffsequence to next instance of branch
    
    # WARNING! Not entirely sure about self-colliding patterns. I think they are ok. -Y
    
    if iscontradiction:
        print "Configuration "+str(configuration)+" returned contradiction."
    elif not iscontradiction:
        print "Configuration "+str(configuration)+" did not return contradiction."
        
    [rows,cols]=np.shape(collisionMatrix)
    numvertices=rows
    rangenum=np.array(range(numvertices))
    
    on=1
    off=2
    undecided=0
    
    vertexdegrees=np.sum(collisionMatrix, axis=0)
    verticesincr=np.argsort(vertexdegrees)
    undecidedvertices=[vertex for vertex in verticesincr if vertex in rangenum[configuration==undecided]]

    print "Undecided vertices are "+str(undecidedvertices)

    if iscontradiction:
        # if this configuration led to contradiction
        # go back to last vertex which was turned on and change to off
        onvxindices=np.argwhere(onoffsequence==on)
        if len(onvxindices)==0:
            # there are no vertices that are on
            # this is the end of the branching
            print "All vertices in the configuration are off or undecided, and this has given a contradiction. This is the end of the branching. :)"
            return [np.array([]),np.array(None),np.array(None)]
        else:
            # otherwise may safely roll back to last vx which was turned on
            lastonvxindex=onvxindices[-1][0]
            newvertexsequence=np.copy(vertexsequence[:lastonvxindex+1])
            newonoffsequence=np.copy(onoffsequence[:lastonvxindex+1])
            newonoffsequence[-1]=off
            print "Rolling back and turning vertex "+str(newvertexsequence[-1])+" off"
            
            # now generate the configuration given by this vertex sequence
            newconfiguration=np.zeros(numvertices,dtype=int)
            for i in range(len(newvertexsequence)):
                if newonoffsequence[i]==on:
                    vertexnhood=np.copy(collisionMatrix[vertex,:])
                    newconfiguration[newvertexsequence[i]]=on
                    newconfiguration[vertexnhood==1]=off
                elif newonoffsequence[i]==off:
                    newconfiguration[newvertexsequence[i]]=off
            print "The new configuration to try is "+str(newconfiguration)        
            return [newconfiguration,newvertexsequence, newonoffsequence]
        
    elif not iscontradiction:
        # if this configuration hasn't given a contradiction
        # turn on next highest-degree vertex and turn off all vertices in its neighbourhood
        if not undecidedvertices:
            # if there are no undecided vertices left and no contradiction, these constraints are not enough
            print "All vertices in input configuration have been fixed to on/off and still no contradiction occurred. :("
            return [np.array([]),np.array(None),np.array(None)]
        
        elif undecidedvertices:
            # there are some undecided vertices, so go to the max degree one and give it on/off label
            newvertex=undecidedvertices[-1]
            newconfiguration=np.copy(configuration)
            newonoffsequence=np.copy(onoffsequence)
            newvertexsequence=np.append(vertexsequence,newvertex)
            
            if collisionMatrix[newvertex,newvertex]==1:
                # pattern is self-colliding so it must be off
                newconfiguration[newvertex]=off
                newonoffsequence=np.append(newonoffsequence,off)
                print "Turning vertex "+str(newvertex)+" off. Cannot be on as it is self-colliding."

            else:
                # turn on next highest-degree vertex and turn off all vertices in its neighbourhood
                newconfiguration[newvertex]=on
                newvertexnhood=np.copy(collisionMatrix[newvertex,:])
                newconfiguration[newvertexnhood==1]=off
                newonoffsequence=np.append(newonoffsequence,on)
                print "Turning vertex "+str(newvertex)+" on"
                
            print "The new configuration to try is "+str(newconfiguration)        
            return [newconfiguration,newvertexsequence, newonoffsequence]

 
