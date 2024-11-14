# -*- coding: utf-8 -*-
''' Nonlinear non-linear spring model to analyze pile wall structutres.'''

__author__= "Luis C. Pérez Tato (LCPT) , Ana Ortega (AO_O) "
__copyright__= "Copyright 2024, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es, ana.Ortega@ciccp.es "

import xc
from geotechnics import earth_pressure
from scipy.constants import g
from model import predefined_spaces
from solution import predefined_solutions

from operator import itemgetter
from scipy.interpolate import interp1d
from postprocess.reports import common_formats as cf
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

def get_results_table(resultsDict):
    ''' Return the given results in tabular format.

    :param resultsDict: dictionary containing the results.
    '''
    headerRow= ['#', 'fixed node', 'depth (m)', 'Ux (mm)', 'M (kN.m)', 'V (kN)', 'pres. dif. (kN/m)', 'Rx (kN)', 'Ea (kN)', 'E0 (kN)', 'Ep (kN)']
    retval= list()
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
    # Sort on depth
    retval= sorted(retval, key=lambda x: float(x[2]))
    retval.insert(0, headerRow)
    return retval

def plot_results(resultsDict, title= None):
    ''' Return the given results in tabular format.

    :param resultsDict: dictionary containing the results.
    :param title: title.
    '''
    def get_results(resultsDict, x_field:str, x_scale_factor:float, y_field= 'depth'):
        ''' Extract the results from the given dictionary and sort them on
            depth.

        :param resultsDict: dictionary containing the analysis results.
        :param x_field: values for the x axis.
        :param x_scale_factor: scale factor on the x axis.
        :param y_field: values por the y axis.
        '''
        xy= list()
        for nodeTag in resultsDict:
            nodeResults= resultsDict[nodeTag]
            depth= nodeResults[y_field]
            xValue= nodeResults[x_field]
            xy.append((xValue*x_scale_factor, depth))
        ## Sort on depth
        xy= sorted(xy, key=lambda x: float(x[1]))
        ## Unzip the tuples.
        return zip(*xy)

    def plot_diagram(ax, resultsDict, title:str, x_field:str, x_scale_factor:float, x_label:str, y_field= 'depth', y_label= None):
        ''' Extract the results from the given dictionary and sort them on
            depth.

        :param ax: matplotlib Axes object.
        :param resultsDict: dictionary containing the analysis results.
        :param title: title for the diagram.
        :param x_field: values for the x axis.
        :param x_scale_factor: scale factor on the x axis.
        :param x_label: label for the x axis.
        :param y_field: values por the y axis.
        :param y_label: label for the y axis.
        '''
        x, y= get_results(resultsDict= resultsDict, x_field= x_field, x_scale_factor= x_scale_factor, y_field= y_field)
        ax.plot(x, y, diagramsColor)
        ax.invert_yaxis()  # Reverse y-axis
        topPoint= (0.0, y[0])
        bottomPoint= (0.0, y[-1])
        ax.plot([bottomPoint[0], topPoint[0]], [bottomPoint[1], topPoint[1]], pileWallColor) # plot pile wall
        ratio= 4
        xleft, xright = ax.get_xlim()
        ybottom, ytop = ax.get_ylim()
        ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
        if(x_field=='Ux'):
            loc = plticker.MultipleLocator(base=40.0) # this locator puts ticks at regular intervals
            ax.xaxis.set_major_locator(loc)

        if(y_label):
            ax.set(xlabel= x_label, ylabel= y_label)
        else:
            ax.set(xlabel= x_label)
        ax.set_title(title)
        ax.grid()
        
    fig, (disp, moment, shear, presDif, soilReact) = plt.subplots(1, 5)
    pileWallColor= 'tab:blue'
    diagramsColor= 'tab:red'
    # Plot displacements.
    plot_diagram(ax= disp, resultsDict= resultsDict, title= 'Displacements', x_field= 'Ux', x_scale_factor= 1e3, x_label= 'Ux (mm)', y_field= 'depth', y_label= 'Depth (m)')
    
    # Plot bending moment.
    plot_diagram(ax= moment, resultsDict= resultsDict, title= 'Moment', x_field= 'M', x_scale_factor= 1e-3, x_label= '$M (kN \cdot m)$', y_field= 'depth', y_label= None)
    
    # Plot shear forces.
    plot_diagram(ax= shear, resultsDict= resultsDict, title= 'Shear', x_field= 'V', x_scale_factor= 1e-3, x_label= '$V (kN)$', y_field= 'depth', y_label= None)
    
    # Plot pDif.
    plot_diagram(ax= presDif, resultsDict= resultsDict, title= 'Pres. Dif.', x_field= 'pDif', x_scale_factor= 1e-3, x_label= '$pD (kN/m)$', y_field= 'depth', y_label= None)
    
    # Plot soil reactions.
    plot_diagram(ax= soilReact, resultsDict= resultsDict, title= 'Soil Reac.', x_field= 'Rx', x_scale_factor= 1e-3, x_label= '$Rx (kN)$', y_field= 'depth', y_label= None)

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
    :ivar soils: soil objects for each layer.
    :ivar waterTableDepthIndex: index of the water table depth in self.depths.
    :ivar excavationDepthIndex: index of the excavation depth in self.depths.
    '''
    def __init__(self, depths, soils, waterTableDepth= None, excavationDepth= None):
        '''Constructor.

        :param depths: (float list) layer depths.
        :param soils: soil objects for each layer.
        :param waterTableDepth: depth of the water table.
        '''
        self.depths= depths
        self.soils= soils
        self.setWaterTableDepth(waterTableDepth= waterTableDepth)
        self.setExcavationDepth(excavationDepth= excavationDepth)

    def getTotalDepth(self):
        ''' Return the distance from the deepest to the shallwest depth in the
            contariner.
        '''
        return self.depths[-1]-self.depths[0]
        
    def splitAtDepth(self, newDepth= None):
        ''' Recomputes the depths and soils list to take account of
            the given one.
        :param newDepth: depth of interest.
        '''
        retval= -1
        if(newDepth):
            calculationDepths= list()
            calculationSoils= list()
            newDepthIndex= self.getSoilIndexAtDepth(depth= newDepth)
            # Check if already in depths list.
            soilDepth= self.depths[newDepthIndex]
            totalDepth= self.getTotalDepth()
            tol= totalDepth/1e3
            if(abs(soilDepth-newDepth)>tol): # not in depths list.
                for i, (d, soil) in enumerate(zip(self.depths, self.soils)):
                    calculationDepths.append(d)
                    calculationSoils.append(soil)
                    if(i==newDepthIndex):
                        calculationDepths.append(newDepth)
                        calculationSoils.append(soil)
                        retval= newDepthIndex+1
                self.depths= calculationDepths
                self.soils= calculationSoils
            else:
                retval= newDepthIndex
        return retval
            
    def setWaterTableDepth(self, waterTableDepth= None):
        ''' Recomputes the depths and soils list to take account of
            the water table.

        :param waterTableDepth: depth of the water table.
        '''
        self.waterTableDepthIndex= self.splitAtDepth(waterTableDepth)
        
    def setExcavationDepth(self, excavationDepth= None):
        ''' Recomputes the depths and soils list to take account of
            the water table.

        :param excavationDepth: depth of the water table.
        '''
        self.excavationDepthIndex= self.splitAtDepth(excavationDepth)
        
    def getWaterTableDepth(self):
        ''' Return the index that corresponds to the depth of the water table.
        '''
        retval= 6378e3
        if(self.waterTableDepthIndex>0):
            retval= self.depths[self.waterTableDepthIndex]
        return retval
        
    def getExcavationDepth(self):
        ''' Return the index that corresponds to the excavation depth.
        '''
        retval= 6378e3
        if(self.excavationDepthIndex>0):
            retval= self.depths[self.excavationDepthIndex]
        return retval

    def getDepths(self):
        ''' Return the depths of the different soil strata.'''
        return self.depths

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

    
class PileWall(object):
    '''Pile wall analysis using non-linear spring to represent soil-structure
       interaction.

    :ivar pileSection: 2D elastic shear section for the pile wall beam elements.
    :ivar soilLayers: SoilLayers object.
    '''
    
    def __init__(self, pileSection, soilLayersDepths, soilLayers, excavationDepth, pileSpacing= 1.0, waterTableDepth= None):
        '''Constructor.

        :param pileSection: 2D elastic shear section for the pile wall beam
                            elements.
        :param soilLayersDepths: (float list) layer depths.
        :param soilLayers: soil object for each layer.
        :param excavationDepth: depth of the excavation.
        :param pileSpacing: distance between pile axes.
        :param waterTableDepth: (float) depth of the water table.
        '''
        self.pileSection= pileSection
        self.soilLayers= SoilLayers(depths= soilLayersDepths, soils= soilLayers, waterTableDepth= waterTableDepth, excavationDepth= excavationDepth)
        self.pileSpacing= pileSpacing

    def defineFEProblem(self):
        ''' Define the FE problem.'''
        self.feProblem= xc.FEProblem()
        preprocessor=  self.feProblem.getPreprocessor   
        nodes= preprocessor.getNodeHandler
        ## Problem type
        self.modelSpace= predefined_spaces.StructuralMechanics2D(nodes)
        # Solution procedure. 
        #solProc= predefined_solutions.PenaltyKrylovNewton(prb= feProblem, numSteps= numSteps, maxNumIter= 300, convergenceTestTol= 1e-6, printFlag= 0)
        self.solProc= predefined_solutions.PenaltyNewtonRaphson(prb= self.feProblem, numSteps= 10, maxNumIter= 300, convergenceTestTol= 1e-5, printFlag= 0)
        
    def setNodeSoils(self):
        ''' Compute the soil corresponding to each node.'''
        self.soilsAtNodes= dict()
        for n in self.pileSet.nodes:
            nodeDepth= -n.getInitialPos3d.y
            nodeSoil= self.soilLayers.getSoilAtDepth(nodeDepth)
            self.soilsAtNodes[n.tag]= nodeSoil
            
    def genMesh(self):
        '''Define the FE mesh.

        :param modelSpace:
        '''
        # Define finite element problem.
        self.defineFEProblem()
        preprocessor= self.feProblem.getPreprocessor
        
        # Problem geometry
        lines= list()
        kPoints= list()
        for depth in self.soilLayers.getDepths():
            kPoints.append(self.modelSpace.newKPoint(0,-depth,0))
        kPt0= kPoints[0]
        for kPt1 in kPoints[1:]:
            newLine= self.modelSpace.newLine(kPt0, kPt1)
            newLine.setElemSize(0.25)
            kPt0= kPt1
            lines.append(newLine)
        
        # Mesh generation
        ## FE material.
        xcPileSection= self.pileSection.defElasticShearSection2d(preprocessor)
        ## Geometric transformations
        lin= self.modelSpace.newLinearCrdTransf("lin")
        ## Seed element
        seedElemHandler= preprocessor.getElementHandler.seedElemHandler
        seedElemHandler.dimElem= 2 # Bars defined in a two-dimensional space.
        seedElemHandler.defaultMaterial= xcPileSection.name
        seedElemHandler.defaultTransformation= lin.name
        beam2d= seedElemHandler.newElement("ElasticBeam2d")
        # beam2d.h= diameter
        self.pileSet= self.modelSpace.defSet('pileSet')
        for ln in lines:
            ln.genMesh(xc.meshDir.I)
            self.pileSet.lines.append(ln)
        self.pileSet.fillDownwards()

        ## Constraints.
        bottomNode= kPoints[-1].getNode()
        self.modelSpace.fixNodeF0F(bottomNode.tag) # Fix vertical displacement.

        ### Define soil response diagrams.
        soilResponseMaterials= dict()
        self.tributaryAreas= dict()
        #### Compute tributary lengths.
        self.pileSet.resetTributaries()
        self.pileSet.computeTributaryLengths(False) # Compute tributary lenghts.
        #### Compute soils at nodes.
        self.setNodeSoils()
        #### Define non-linear springs.
        for n in self.pileSet.nodes:
            nodeDepth= -n.getInitialPos3d.y
            nonLinearSpringMaterial= None
            tributaryArea= 0.0
            if(nodeDepth>0.0): # Avoid zero soil response.
                tributaryLength= n.getTributaryLength()
                tributaryArea= tributaryLength*self.pileSpacing
                materialName= 'soilResponse_z_'+str(n.tag)
                nodeSoil= self.soilsAtNodes[n.tag]
                nonLinearSpringMaterial= nodeSoil.defHorizontalSubgradeReactionNlMaterial(preprocessor, name= materialName, depth= nodeDepth, tributaryArea= tributaryArea, Kh= nodeSoil.Kh)

            self.tributaryAreas[n.tag]= tributaryArea
            soilResponseMaterials[n.tag]= nonLinearSpringMaterial

        ### Duplicate nodes below ground level.
        self.springPairs= list()
        for n in self.pileSet.nodes:
            nodeTag= n.tag
            if(nodeTag in soilResponseMaterials):
                newNode= self.modelSpace.duplicateNode(n)
                self.modelSpace.fixNode000(newNode.tag)
                self.springPairs.append((n, newNode))

        ### Define Spring Elements
        elements= preprocessor.getElementHandler
        elements.dimElem= 2 #Element dimension.
        self.leftZLElements= dict()
        self.rightZLElements= dict()
        for i, pair in enumerate(self.springPairs):
            nodeTag= pair[0].tag
            soilResponseMaterial= soilResponseMaterials[nodeTag]
            if(soilResponseMaterial): # Spring defined for this node.
                # Material for the left spring
                elements.defaultMaterial= soilResponseMaterial.name
                # Springs on the left side of the beam
                zlLeft= elements.newElement("ZeroLength",xc.ID([pair[1].tag, pair[0].tag]))
                zlLeft.setupVectors(xc.Vector([-1,0,0]),xc.Vector([0,-1,0]))
                self.leftZLElements[nodeTag]= zlLeft

                # Springs on the right side of the beam
                zlRight= elements.newElement("ZeroLength",xc.ID([pair[0].tag, pair[1].tag]))
                zlRight.setupVectors(xc.Vector([1,0,0]),xc.Vector([0,1,0]))
                self.rightZLElements[nodeTag]= zlRight
                
    def updateSpringStiffness(self, remainingLeftElements, currentExcavationDepth):
        ''' Update the stiffness of the remaining materials after each 
            excavation step.

        :param remainingLeftElements: elements that remain "alive".
        :param currentExcavationDepth: current excavation depth.
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
            soil= self.soilsAtNodes[nodeTag]
            newEa, newE0, newEp= soil.getEarthThrusts(depth= newDepth, tributaryArea= self.tributaryAreas[nodeTag])
            # Update soil response.
            leftElementInitStrainMaterial= leftElement.getMaterials()[0]
            leftElementEyBasicMaterial= leftElementInitStrainMaterial.material

            leftElementEyBasicMaterial.setParameters(soil.Kh, -newEp, -newEa)
            leftElementInitStrainMaterial.setInitialStress(-newE0)
            updatedElements.append(leftElement)
            #print('node: ', nodeTag, ' node depth: ', '{:.2f}'.format(nodeDepth), ' left node depth: ', '{:.2f}'.format(newDepth), ' tributary area: ', '{:.2f}'.format(tributaryAreas[nodeTag]), 'strains: ', oldInitStrain, -newInitStrain, newInitStrain+oldInitStrain, ' elementTag= ', leftElement.tag)
        return updatedElements
    
    def excavationProcess(self, excavationSide):
        ''' Deactivates the excavated elements and updates the stiffness of the
            remaining ones.

        :param excavationSide: side for the excavation ('left' or 'right')
        '''
        self.nodesToExcavate= list() # Nodes in the excavation depth.
        excavationDepth= self.soilLayers.getExcavationDepth()
        for n in self.pileSet.nodes:
            nodeDepth= -n.getInitialPos3d.y
            print(n.tag, nodeDepth, excavationDepth)
            if(nodeDepth<=excavationDepth):
                self.nodesToExcavate.append((nodeDepth, n))
        ## Sort nodes to excavate on its depth
        self.nodesToExcavate.sort(key=itemgetter(0))
        ## Elements on excavation side.
        elementsOnExcavationSide= None
        if(excavationSide=='left'):
            elementsOnExcavationSide= self.leftZLElements
        elif(excavationSide=='right'):
            elementsOnExcavationSide= self.rightZLElements
        else:
            lmsg.error("Excavation side can be 'left' or 'right'.")
            exit(1)
        ## Elements to deactivate.
        remainingLeftElements= elementsOnExcavationSide
        excavationDepth= self.soilLayers.getExcavationDepth()
        for tp in self.nodesToExcavate:
            currentExcavationDepth= tp[0]
            if(currentExcavationDepth>excavationDepth): # if excavation depth is reached, stop.
                break
            node= tp[1]
            nodeTag= node.tag
            leftSpring= None
            if(nodeTag in remainingLeftElements): # left spring still exists.
                leftSpring= remainingLeftElements[nodeTag]
                if(leftSpring):
                    # remove the spring.
                    toKill= self.modelSpace.defSet('kill'+str(leftSpring.tag))
                    toKill.getElements.append(leftSpring)
                    toKill.killElements()
                    remainingLeftElements.pop(nodeTag) # remove it from the dictionary.
                    ok= self.solProc.solve()
                    if(ok!=0):
                        lmsg.error('Can\'t solve')
                        exit(1)
                    # Update left springs.
                    updatedElements= self.updateSpringStiffness(remainingLeftElements, currentExcavationDepth= currentExcavationDepth)
                    # Solve again.
                    ok= self.solProc.solve()
                    if(ok!=0):
                        lmsg.error('Can\'t solve')
                        exit(1)
        return updatedElements
                
    def solve(self, reactionCheckTolerance= 1e-6, excavationSide= 'left'):
        '''Compute the solution.

        :param reactionCheckTolerance: tolerance when checking nodal reactions.
        :param excavationSide: side for the excavation ('left' or 'right')
        '''
        ok= self.solProc.solve()
        if(ok!=0):
            lmsg.error('Can\'t solve')
            exit(1)
            
        updatedElements= self.excavationProcess(excavationSide= excavationSide)
        self.modelSpace.calculateNodalReactions(reactionCheckTolerance= reactionCheckTolerance)

    def getResultsDict(self):
        ''' Extracts earth pressures and internal forces from the model.'''
        retval= dict()
        for sp in self.springPairs:
            fixedNode= sp[1]
            Rx= fixedNode.getReaction[0]
            pileNode= sp[0]
            Ux= pileNode.getDisp[0]
            depth= -fixedNode.getInitialPos3d.y
            soil= self.soilsAtNodes[pileNode.tag]
            tributaryArea= self.tributaryAreas[pileNode.tag]
            Ea, E0, Ep= soil.getEarthThrusts(depth= depth, tributaryArea= tributaryArea)
            nodeResults= {'depth': depth, 'fixed_node':fixedNode.tag, 'Rx':Rx, 'E0':E0, 'Ea':Ea, 'Ep':Ep, 'Ux':Ux}
            # if(pileNode.tag in leftZLElements):
            #     leftElement= leftZLElements[pileNode.tag]
            #     leftN= leftElement.getResistingForce()[0]
            #     rightElement= rightZLElements[pileNode.tag]
            #     rightN= rightElement.getResistingForce()[0]
            #     print('  leftN= ', leftN/1e3, 'rightN= ', rightN/1e3)
            retval[pileNode.tag]= nodeResults
        # Get internal forces.
        for ln in self.pileSet.lines: # for lines in list
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
        for ln in self.pileSet.lines: # for lines in list
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

