# -*- coding: utf-8 -*-
''' Nonlinear soil spring model inspired in the example 14.2 of the book "Principles of Foundation Engineering" of Braja M. Das. Eight Edition. CENGAGE Learning. 2016.'''

from operator import itemgetter

# Excavation process.
def update_spring_stiffness(remainingLeftElements, currentExcavationDepth, tributaryAreas, soil, Kh):
    ''' Update the stiffness of the remaining materials after each excavation
        step.

    :param remainingLeftElements: elements that remain "alive".
    :param currentExcavationDepth: current excavation depth.
    :param tributaryAreas: dictionary containing the tributary areas corresponding to each node.
    :param soil: soil model to compute the soil reaction diagram.
    :param Kh: horizontal subgrade reaction modulus.
    '''
    updatedElements= list()
    for nodeTag in remainingLeftElements:
        leftElement= remainingLeftElements[nodeTag]
        elemNodes= leftElement.nodes
        # Get the node depth.
        nodeIndex= 1
        if(nodeTag==elemNodes[0].tag):
            nodeIndex= 0
        pileNode= elemNodes[nodeIndex]
        nodeDepth= -pileNode.getInitialPos3d.y
        newDepth= nodeDepth-currentExcavationDepth
        # Compute new soil response.
        newEa, newE0, newEp= soil.getEarthThrusts(depth= newDepth, tributaryArea= tributaryAreas[nodeTag])
        # Update soil response.
        leftElementInitStrainMaterial= leftElement.getMaterials()[0]
        leftElementEyBasicMaterial= leftElementInitStrainMaterial.material

        leftElementEyBasicMaterial.setParameters(Kh, -newEp, -newEa)
        leftElementInitStrainMaterial.setInitialStress(-newE0)
        updatedElements.append(leftElement)
        #print('node: ', nodeTag, ' node depth: ', '{:.2f}'.format(nodeDepth), ' left node depth: ', '{:.2f}'.format(newDepth), ' tributary area: ', '{:.2f}'.format(tributaryAreas[nodeTag]), 'strains: ', oldInitStrain, -newInitStrain, newInitStrain+oldInitStrain, ' elementTag= ', leftElement.tag)
    return updatedElements
                    
def excavation_process(preprocessor, solProc, nodesToExcavate, elementsOnExcavationSide, maxDepth, tributaryAreas, soil, Kh):
    ''' Deactivates the excavated elements and updates the stiffness of the
        remaining ones.

    :param preprocessor: pre-processor of the finite element problem.
    :param solProc: solution procedure.
    :param nodesToExcavate: nodes that lie on the excavation depth.
    :param elementsOnExcavationSide: elements that lie on the excavation side.
    :param maxDepth: maximum excavation depth.
    :param tributaryAreas: dictionary containing the tributary areas corresponding to each node.
    :param soil: soil model to compute the soil reaction diagram.
    :param Kh: horizontal subgrade reaction modulus.
    '''
    ## Sort nodes to excavate on its depth
    nodesToExcavate.sort(key=itemgetter(0))
    ## Elements to deactivate.
    remainingLeftElements= elementsOnExcavationSide
    for tp in nodesToExcavate:
        currentExcavationDepth= tp[0]
        if(currentExcavationDepth>maxDepth):
            break
        node= tp[1]
        nodeTag= node.tag
        leftSpring= None
        if(nodeTag in remainingLeftElements): # left spring still exists.
            leftSpring= remainingLeftElements[nodeTag]
            if(leftSpring):
                # remove the spring.
                toKill= preprocessor.getSets.defSet('kill'+str(leftSpring.tag))
                toKill.getElements.append(leftSpring)
                toKill.killElements()
                remainingLeftElements.pop(nodeTag) # remove it from the dictionary.
                ok= solProc.solve()
                if(ok!=0):
                    lmsg.error('Can\'t solve')
                    exit(1)
                # Update left springs.
                updatedElements= update_spring_stiffness(remainingLeftElements, currentExcavationDepth= currentExcavationDepth, tributaryAreas= tributaryAreas, soil= soil, Kh= Kh)
                # Solve again.
                ok= solProc.solve()
                if(ok!=0):
                    lmsg.error('Can\'t solve')
                    exit(1)
    return updatedElements
