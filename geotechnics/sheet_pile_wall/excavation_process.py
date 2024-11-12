# -*- coding: utf-8 -*-
''' Nonlinear soil spring model inspired in the example 14.2 of the book "Principles of Foundation Engineering" of Braja M. Das. Eight Edition. CENGAGE Learning. 2016.'''

from geotechnics import earth_pressure
from scipy.constants import g

from operator import itemgetter
from scipy.interpolate import interp1d
from postprocess.reports import common_formats as cf
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# Excavation process.
def update_spring_stiffness(remainingLeftElements, currentExcavationDepth, tributaryAreas, soil):
    ''' Update the stiffness of the remaining materials after each excavation
        step.

    :param remainingLeftElements: elements that remain "alive".
    :param currentExcavationDepth: current excavation depth.
    :param tributaryAreas: dictionary containing the tributary areas corresponding to each node.
    :param soil: soil model to compute the soil reaction diagram.
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

        leftElementEyBasicMaterial.setParameters(soil.Kh, -newEp, -newEa)
        leftElementInitStrainMaterial.setInitialStress(-newE0)
        updatedElements.append(leftElement)
        #print('node: ', nodeTag, ' node depth: ', '{:.2f}'.format(nodeDepth), ' left node depth: ', '{:.2f}'.format(newDepth), ' tributary area: ', '{:.2f}'.format(tributaryAreas[nodeTag]), 'strains: ', oldInitStrain, -newInitStrain, newInitStrain+oldInitStrain, ' elementTag= ', leftElement.tag)
    return updatedElements
                    
def excavation_process(preprocessor, solProc, nodesToExcavate, elementsOnExcavationSide, maxDepth, tributaryAreas, soil):
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
                updatedElements= update_spring_stiffness(remainingLeftElements, currentExcavationDepth= currentExcavationDepth, tributaryAreas= tributaryAreas, soil= soil)
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

class SoilLayers(object):
    '''Layers of different soils.

    Soil with layers of different properties as described in
    4.5.5.7 "Guía de cimentaciones en obras de carreteras"
    (https://books.google.ch/books?id=a0eoygAACAAJ)
    2009

    :ivar depths: (float list) layer depths.
    :ivar soils: (float list) soil for each layer.
    :ivar waterTableDepth: (float list) depth of the water table.
    '''
    def __init__(self, depths, soils, waterTableDepth= None):
        '''Constructor.

        :param depths: (float list) layer depths.
        :param soils: (float list) soil for each layer.
        :param waterTableDepth: (float list) depth of the water table.
        '''
        self.depths= depths
        self.soils= soils
        self.setWaterTableDepth(waterTableDepth= waterTableDepth)

    def setWaterTableDepth(self, waterTableDepth= None):
        ''' Recomputes the depths and soils list to take account of
            the water table.
        :param waterTableDepth: (float list) depth of the water table.
        '''
        if(waterTableDepth):
            calculationDepths= list()
            calculationSoils= list()
            waterTableDepthIndex= self.getSoilIndexAtDepth(depth= waterTableDepth)
            # Check if already in depths list.
            soilDepth= self.depths[waterTableDepthIndex]
            if(abs(soilDepth-waterTableDepth)>1e-5): # not in depths list.
                for i, (d, soil) in enumerate(zip(self.depths, self.soils)):
                    calculationDepths.append(d)
                    calculationSoils.append(soil)
                    if(i==waterTableDepthIndex):
                        calculationDepths.append(waterTableDepth)
                        calculationSoils.append(soil)
                        self.waterTableDepthIndex= waterTableDepthIndex+1
                self.depths= calculationDepths
                self.soils= calculationSoils
            else:
                self.waterTableDepthIndex= waterTableDepthIndex
        
    def getWaterTableDepth(self):
        ''' Return the index that corresponds to water table depth.

        '''
        return self.depths[self.waterTableDepthIndex]

    def getSoilIndexAtDepth(self, depth):
        ''' Return the index of the soil corresponding to the given depth.

        :param depth: depth of interest.
        '''
        retval= -1
        for i, d in enumerate(self.depths):
            if(depth>=d):
                retval= i
        return retval

    def getSoilAtDepth(self, depth):
        ''' Return the soil corresponding to the given depth.

        :param depth: depth of interest.
        '''
        retval= None
        soilIndex= self.getSoilIndexAtDepth(depth= depth)
        if(soilIndex>=0):
            retval= self.soils[soilIndex]
        return retval
    
    def getHydrostaticPressureAtDepth(self, depth):
        ''' Returns the hydrostatic presure at the given depth.

        :param depth: depth to compute the pressure at.
        '''
        retval= 0.0
        waterTableDepth= self.getWaterTableDepth()
        if(depth>waterTableDepth):
            retval= 1e3*g*(depth-waterTableDepth)
        return retval

    def getVerticalPressureAtDepth(self, depth):
        ''' Returns the vertical presure at the given depth.

        :param depth: depth to compute the pressure at.
        '''
        retval= 0.0
        if(depth>self.depths[0]):
          lastDepth= self.depths[0]
          for i, d in enumerate(self.depths):
              soil= self.soils[i]
              gamma= soil.gamma()
              currentDepth= min(depth, d)
              if(currentDepth>self.getWaterTableDepth()):
                  gamma= soil.submergedGamma()
              soilThickness= currentDepth-lastDepth
              retval+= gamma*soilThickness
              if(abs(currentDepth-depth)<1e-6):
                  break
              lastDepth= d
        return retval
        
    def getHorizontalPressureAtDepth(self, K, depth):
        ''' Returns the horizontal presure at the given depth.

        :param K: pressure coefficient.
        :param depth: depth to compute the pressure at.
        '''
        return self.getVerticalPressureAtDepth(depth= depth)*K

    def getActivePressureAtDepth(self, depth, designValue= False):
        ''' Returns the active presure at the given depth.

        :param depth: depth to compute the pressure at.
        :param waterTableDepth: depth of the water table.
        :param designValue: if true use the design value of the internal 
                            friction.
        '''
        soil= self.getSoilAtDepth(depth= depth)
        Ka= soil.Ka(designValue= designValue)
        return self.getHorizontalPressureAtDepth(K= Ka, depth= depth)
    
    def getPassivePressureAtDepth(self, depth, designValue= False):
        ''' Returns the passive presure at the given depth.

        :param depth: depth to compute the pressure at.
        :param waterTableDepth: depth of the water table.
        :param designValue: if true use the design value of the internal 
                            friction.
        '''
        soil= self.getSoilAtDepth(depth= depth)
        Kp= soil.Kp(designValue= designValue)
        return self.getHorizontalPressureAtDepth(K= Kp, depth= depth)
    
    def getAtRestPressureAtDepth(self, depth, designValue= False):
        ''' Returns the at-rest presure at the given depth.

        :param depth: depth to compute the pressure at.
        :param waterTableDepth: depth of the water table.
        :param designValue: if true use the design value of the internal 
                            friction.
        '''
        soil= self.getSoilAtDepth(depth= depth)
        K0= soil.K0Jaky(designValue= designValue)
        return self.getHorizontalPressureAtDepth(K= K0, depth= depth)

    def getEarthThrusts(self, depth, tributaryArea, waterTableDepth= 6371e3, designValue= False):
        ''' Returns the active, at-rest and passive presure at the given depth.

        :param depth: depth to compute the pressure.
        :param tributaryArea: area on which the pressure acts.
        :param waterTableDepth: depth of the water table.
        :param designValue: if true use the design value of the internal 
                            friction.
        '''

        Ea= self.getActivePressureAtDepth(depth= depth, designValue= designValue)*tributaryArea # active.
        E0= self.getAtRestPressureAtDepth(depth= depth, designValue= designValue)*tributaryArea # at rest.
        Ep= self.getPassivePressureAtDepth(depth= depth, designValue= designValue)*tributaryArea # passive.
        return Ea, E0, Ep
    
    def defHorizontalSubgradeReactionNlMaterialAtDepth(self, preprocessor, name, depth, tributaryArea, designValue= False):
        ''' Return the points of the force-displacement diagram.

        :param preprocessor: preprocessor of the finite element problem.
        :param name: name identifying the material (if None compute a suitable name)
        :param depth: depth of the point of interest.
        :param tributaryArea: area on which the pressure acts.
        :param designValue: if true use the design value of the internal 
                            friction.
        '''
        # Compute corresponding earth thrusts (active, at rest, passive).
        Ea, E0, Ep= self.getEarthThrusts(depth= depth, tributaryArea= tributaryArea, designValue= designValue)
        # Define nonlinear spring material
        matName= name
        if(not matName):
            matName= uuid.uuid1().hex            
        eyMatName= 'ey'+matName
        soil= self.getSoilAtDepth(depth= depth)
        eyBasicMaterial= earth_pressure.def_ey_basic_material(preprocessor, name= eyMatName, E= soil.Kh, upperYieldStress= -Ea, lowerYieldStress= -Ep)
        # Create initial stress material.
        materialHandler= preprocessor.getMaterialHandler
        retval= materialHandler.newMaterial("init_stress_material", matName)
        retval.setMaterial(eyBasicMaterial.name)
        retval.setInitialStress(-E0)
        return retval
