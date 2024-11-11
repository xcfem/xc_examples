# -*- coding: utf-8 -*-
''' Nonlinear soil spring model inspired in the example 14.2 of the book "Principles of Foundation Engineering" of Braja M. Das. Eight Edition. CENGAGE Learning. 2016.'''

from operator import itemgetter
from scipy.interpolate import interp1d
from postprocess.reports import common_formats as cf
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

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
    :param tributaryAreas: dictionary containing the tributary areas 
                           corresponding to each node.
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

def get_results_dict(tributaryAreas, soil, springPairs, pileWallElements):
    ''' Extracts earth pressures and internal forces from the model.

    :param tributaryAreas: dictionary containing the tributary areas 
                           corresponding to each node.
    :param soil: soil model to compute the soil reaction diagram.
    :param springPairs: pairs of nodes at the extremities of the springs
                        elements representing the soil.
    :param pileWallElements: top-down list of consecutive lines that compose
                             the pile wall.
    '''
    retval= dict()
    e0_factor= soil.K0Jaky()*soil.gamma()
    ea_factor= soil.Ka()*soil.gamma()
    ep_factor= soil.Kp()*soil.gamma()
    for sp in springPairs:
        fixedNode= sp[1]
        Rx= fixedNode.getReaction[0]
        pileNode= sp[0]
        Ux= pileNode.getDisp[0]
        depth= -fixedNode.getInitialPos3d.y
        tributaryArea= tributaryAreas[pileNode.tag]
        E0= e0_factor*tributaryArea*depth
        Ea= ea_factor*tributaryArea*depth
        Ep= ep_factor*tributaryArea*depth
        nodeResults= {'depth': depth, 'fixed_node':fixedNode.tag, 'Rx':Rx, 'E0':E0, 'Ea':Ea, 'Ep':Ep, 'Ux':Ux}
        # if(pileNode.tag in leftZLElements):
        #     leftElement= leftZLElements[pileNode.tag]
        #     leftN= leftElement.getResistingForce()[0]
        #     rightElement= rightZLElements[pileNode.tag]
        #     rightN= rightElement.getResistingForce()[0]
        #     print('  leftN= ', leftN/1e3, 'rightN= ', rightN/1e3)
        retval[pileNode.tag]= nodeResults
    # Get internal forces.
    for ln in pileWallElements: # for lines in list
        for e in ln.elements: # for elements in line.
            nodeTag= e.getNodes[0].tag
            nodeResults= retval[nodeTag]
            depth= nodeResults['depth']
            # M2= e.getM2
            nodeResults['M']= e.getM1 # bending moment.
            nodeResults['V']= e.getV1 # shear force.    
    # Get the moment in the deepest node.
    nodeTag= e.getNodes[1].tag
    retval[nodeTag]['M']= e.getM2 # bending moment.
    retval[nodeTag]['V']= e.getV2 # shear force.
    
    # Compute pres. dif.
    x= list()
    y= list()
    for ln in pileWallElements: # for lines in list
        for e in ln.elements: # for elements in line.
            topNodeTag= e.getNodes[0].tag
            topDepth= retval[topNodeTag]['depth']
            V1= retval[topNodeTag]['V'] # shear force at top node.
            bottomNodeTag= e.getNodes[1].tag
            bottomDepth= retval[bottomNodeTag]['depth']
            V2= retval[bottomNodeTag]['V'] # shear force at bottom node.
            presDif= (V2-V1)/(bottomDepth-topDepth)
            avgDepth= (bottomDepth+topDepth)/2.0
            x.append(avgDepth)
            y.append(presDif)
    presDif= interp1d(x, y, kind='linear', fill_value= 'extrapolate', assume_sorted=True)
    for nodeTag in retval:
        nodeResults= retval[nodeTag]
        depth= nodeResults['depth']
        pDif= presDif(depth)
        nodeResults['pDif']= pDif
    return retval

def get_results_table(resultsDict):
    ''' Return the given results in tabular format.

    :param resultsDict: dictionary containing the results.
    '''
    headerRow= ['#', 'fixed node', 'depth (m)', 'Ux (mm)', 'M (kN.m)', 'V (kN)', 'pres. dif. (kN/m)', 'Rx (kN)', 'Ea (kN)', 'E0 (kN)', 'Ep (kN)']
    retval= [headerRow]
    for nodeTag in resultsDict:
        nodeResults= resultsDict[nodeTag]
        outputRow= [str(nodeTag)] # node tag of the pile wall.
        outputRow.append(str(nodeResults['fixed_node'])) # identifier of the fixed node.
        outputRow.append(cf.Length.format(nodeResults['depth'])) # depth of the node.
        outputRow.append(cf.Length.format(nodeResults['Ux']*1e3)) # displacement of the node.    
        outputRow.append(cf.Force.format(nodeResults['M']/1e3)) # bending moment at the node.
        outputRow.append(cf.Force.format(nodeResults['V']/1e3)) # shear force at the node.
        outputRow.append(cf.Force.format(nodeResults['pDif']/1e3)) # shear force at the node.
        outputRow.append(cf.Force.format(nodeResults['Rx']/1e3)) # reaction of the soil.
        outputRow.append(cf.Force.format(nodeResults['Ea']/1e3)) # active force.
        outputRow.append(cf.Force.format(nodeResults['E0']/1e3)) # at-rest force.
        outputRow.append(cf.Force.format(nodeResults['Ep']/1e3)) # passive force.
        retval.append(outputRow)
    return retval

def plot_results(resultsDict, title= None):
    ''' Return the given results in tabular format.

    :param resultsDict: dictionary containing the results.
    :param title: title.
    '''
    fig, (disp, moment, shear, presDif, soilReact) = plt.subplots(1, 5)
    pileWallColor= 'tab:blue'
    diagramsColor= 'tab:red'
    # Plot displacements.
    x= list()
    y= list()
    for nodeTag in resultsDict:
        nodeResults= resultsDict[nodeTag]
        depth= nodeResults['depth']
        Ux= nodeResults['Ux']
        y.append(depth)
        x.append(Ux*1e3)
    disp.plot(x, y, diagramsColor)
    disp.invert_yaxis()  # Reverse y-axis
    topPoint= (0.0, y[0])
    bottomPoint= (0.0, y[-1])
    disp.plot([bottomPoint[0], topPoint[0]], [bottomPoint[1], topPoint[1]], pileWallColor) # plot pile wall
    ratio= 4
    xleft, xright = disp.get_xlim()
    ybottom, ytop = disp.get_ylim()
    disp.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    loc = plticker.MultipleLocator(base=40.0) # this locator puts ticks at regular intervals
    disp.xaxis.set_major_locator(loc)

    disp.set(xlabel= 'Ux (mm)', ylabel= 'Depth (m)')
    disp.set_title('Displacements')
    disp.grid()
    
    # Plot bending moment.
    x= list()
    y= list()
    for nodeTag in resultsDict:
        nodeResults= resultsDict[nodeTag]
        depth= nodeResults['depth']
        M= nodeResults['M']
        y.append(depth)
        x.append(M/1e3)
    moment.plot([bottomPoint[0], topPoint[0]], [bottomPoint[1], topPoint[1]], pileWallColor) # plot pile wall
    moment.plot(x, y, diagramsColor)
    moment.invert_yaxis()  # Reverse y-axis
    ratio= 4
    xleft, xright = moment.get_xlim()
    ybottom, ytop = moment.get_ylim()
    moment.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    #loc = plticker.MultipleLocator(base=40.0) # this locator puts ticks at regular intervals
    # moment.xaxis.set_major_locator(loc)

    moment.set(xlabel= '$M (kN \cdot m)$')#, ylabel= 'Depth (m)')
    moment.set_title('Moment')
    moment.grid()
    
    # Plot shear forces.
    x= list()
    y= list()
    for nodeTag in resultsDict:
        nodeResults= resultsDict[nodeTag]
        depth= nodeResults['depth']
        V= nodeResults['V']
        y.append(depth)
        x.append(V/1e3)
    shear.plot([bottomPoint[0], topPoint[0]], [bottomPoint[1], topPoint[1]], pileWallColor) # plot pile wall
    shear.plot(x, y, diagramsColor)
    shear.invert_yaxis()  # Reverse y-axis
    ratio= 4
    xleft, xright = shear.get_xlim()
    ybottom, ytop = shear.get_ylim()
    shear.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    #loc = plticker.MultipleLocator(base=40.0) # this locator puts ticks at regular intervals
    # shear.xaxis.set_major_locator(loc)

    shear.set(xlabel= '$V (kN)$')#, ylabel= 'Depth (m)')
    shear.set_title('Shear')
    shear.grid()
    
    # Plot shear forces.
    x= list()
    y= list()
    for nodeTag in resultsDict:
        nodeResults= resultsDict[nodeTag]
        depth= nodeResults['depth']
        pDif= nodeResults['pDif']
        y.append(depth)
        x.append(pDif/1e3)
    presDif.plot([bottomPoint[0], topPoint[0]], [bottomPoint[1], topPoint[1]], pileWallColor) # plot pile wall
    presDif.plot(x, y, diagramsColor)
    presDif.invert_yaxis()  # Reverse y-axis
    ratio= 4
    xleft, xright = presDif.get_xlim()
    ybottom, ytop = presDif.get_ylim()
    presDif.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    #loc = plticker.MultipleLocator(base=40.0) # this locator puts ticks at regular intervals
    # presDif.xaxis.set_major_locator(loc)

    presDif.set(xlabel= '$pD (kN/m)$')#, ylabel= 'Depth (m)')
    presDif.set_title('Pres. Dif.')
    presDif.grid()
    
    # Plot soil reactions.
    x= list()
    y= list()
    for nodeTag in resultsDict:
        nodeResults= resultsDict[nodeTag]
        depth= nodeResults['depth']
        pDif= nodeResults['Rx']
        y.append(depth)
        x.append(pDif/1e3)
    soilReact.plot([bottomPoint[0], topPoint[0]], [bottomPoint[1], topPoint[1]], pileWallColor) # plot pile wall
    soilReact.plot(x, y, diagramsColor)
    soilReact.invert_yaxis()  # Reverse y-axis
    ratio= 4
    xleft, xright = soilReact.get_xlim()
    ybottom, ytop = soilReact.get_ylim()
    soilReact.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    #loc = plticker.MultipleLocator(base=40.0) # this locator puts ticks at regular intervals
    # soilReact.xaxis.set_major_locator(loc)

    soilReact.set(xlabel= '$Rx (kN)$')#, ylabel= 'Depth (m)')
    soilReact.set_title('Soil React.')
    soilReact.grid()

    if(title):
        fig.suptitle(title)
    plt.show()

