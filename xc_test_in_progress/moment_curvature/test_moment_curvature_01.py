# -*- coding: utf-8 -*-
''' Test based on the moment curvature example of the OpenSees documentation.

see: https://opensees.berkeley.edu/wiki/index.php/Moment_Curvature_Example
'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2023, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import ezdxf
import geom
import xc
from model import predefined_spaces
from materials import typical_materials
from solution import predefined_solutions
from materials.sections.fiber_section import plot_fiber_section

#
#        +-----+-----+-----+-----+ J (yJ, zJ)
#        |     |     |     |     |
#        |     |     |     |     |
#        +-----+-----+-----+-----+
#        |     |     |     |     |
#        |     |     |     |     |
#        +-----+-----+-----+-----+
#        |     |     |     |     |
#        |     |     |     |     |
#        +-----+-----+-----+-----+
#        |     |     |     |     |
#        |     |     |     |     |
#        +-----+-----+-----+-----+
#   I (yI, zI)
#
def patch(regions, material, numSubdivY, numSubdivZ, yI, zI, yJ, zJ):
    ''' Emulates the OpenSees "patch rect" command.

    :param regions: region management object.
    :param material: material to fill the region.
    :param numSubdivY:  number of subdivisions (fibers) in the local y direction.
    :param numSubdivZ:  number of subdivisions (fibers) in the local z direction.
    :param yI: y coordinate of vertex I (local coordinate system).
    :param zI: z coordinate of vertex I (local coordinate system).
    :param yJ: y coordinate of vertex J (local coordinate system).
    :param zJ: z coordinate of vertex J (local coordinate system).
    '''
    retval= regions.newQuadRegion(material.name)
    retval.nDivIJ= numSubdivY
    retval.nDivJK= numSubdivZ
    retval.pMin= geom.Pos2d(yI,zI)
    retval.pMax= geom.Pos2d(yJ,zJ)
    return retval

def moment_curvature(modelSpace, section, axialLoad, maxK, numIncr):
    ''' Compute the moment-curvature diagram.

    :param modelSpace: finite element model wrapper.
    :param section: fiber section model.
    :param axialLoad: axial load.
    :param maxK: maximum value of the curvature to reach.
    :param numIncr: number of increments for the analysis.
    '''
    # Define two nodes at (0,0)
    nod1= modelSpace.newNodeXY(0.0, 0.0)
    nod2= modelSpace.newNodeXY(0.0, 0.0)

    # Fix all degrees of freedom except axial and bending
    modelSpace.fixNode000(nod1.tag)
    modelSpace.fixNodeF0F(nod2.tag)

    # Define element
    #                         tag ndI ndJ  secTag
    elements= preprocessor.getElementHandler
    elements.defaultMaterial= section.name
    elements.dimElem= 2 # Dimension of element space
    zl= elements.newElement("ZeroLengthSection",xc.ID([nod1.tag,nod2.tag]))

    # Create recorders
    recDFree= modelSpace.newRecorder("node_prop_recorder",None)
    recDFree.setNodes(xc.ID([nod2.tag]))
    recDFree.callbackRecord= "modelSpace.ti.append(self.getDomain.getTimeTracker.getCurrentTime); modelSpace.ky.append(self.getDisp[2])"
    myRecorder= feProblem.getDomain.newRecorder("element_prop_recorder",None)
    myRecorder.setElements(xc.ID([zl.tag]))
    myRecorder.callbackRecord= "self.getSection().getFibers().getResultant(); modelSpace.mi.append(self.getSection().getFibers().getMz(0.0))"
    myRecorder.callbackSetup= "self.getDomain.calculateNodalReactions(True,1e-4)"

    # Define constant axial load
    loadHandler= modelSpace.getLoadHandler()
    lPatterns= loadHandler.getLoadPatterns
    constantTS= lPatterns.newTimeSeries("constant_ts","constantTS")
    #modelSpace.setCurrentTimeSeries(constantTS.name)
    constantLP= modelSpace.newLoadPattern(name= 'constantLP')
    constantLP.timeSeries= constantTS
    modelSpace.setCurrentLoadPattern(constantLP.name)
    nod2.newLoad(xc.Vector([P,0,0]))
    modelSpace.addLoadCaseToDomain(constantLP.name)

    # Define analysis parameters
    solProc= predefined_solutions.PlainNewtonRaphson(prb= feProblem, printFlag= 1, maxNumIter= 100)
    solProc.setup()
    analysis= solProc.analysis
    
    # Do one analysis for constant axial load
    result= analysis.analyze(1)

    # Define reference moment
    linearTS= lPatterns.newTimeSeries("linear_ts","linearTS")
    #modelSpace.setCurrentTimeSeries(linearTS.name)
    linearLP= modelSpace.newLoadPattern(name= 'linearLP')
    linearLP.timeSeries= linearTS
    modelSpace.setCurrentLoadPattern(linearLP.name)
    nod2.newLoad(xc.Vector([0,0,1]))
    modelSpace.addLoadCaseToDomain(linearLP.name)

    # Compute curvature increment
    dK= maxK/numIncr

    # Use displacement control at node 2 for section analysis
    solProc.integrator= solProc.solutionStrategy.newIntegrator('displacement_control_integrator', solProc.integratorParameters)
    solProc.integrator.nodeTag= nod2.tag
    solProc.integrator.dof= 2
    solProc.integrator.increment= dK
    solProc.integrator.minIncrement= dK
    solProc.integrator.maxIncrement= dK
    #solProc.integrator.setNumIncr(10)

    # Do the section analysis
    analysis.analyze(numIncr)

def plot_diagram(plt, ky, mi):
    ''' Plot the section moment-curvature diagram.

    :plt: matplotlib module.
    :ky: curvature values.
    :mi: bending moment values.
    '''
    plt.plot(ky, mi, "-b")

    # Add title and axis names
    plt.title('Moment-curvature diagram')
    plt.xlabel('curvature')
    plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    plt.xticks(rotation = 90)
    plt.ylabel('bending moment')
    plt.show()

# Define problem
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Define uniaxial materials
## Concrete
confinedConcrete= typical_materials.defConcrete01(preprocessor, 'confinedConcrete', epsc0= -0.004, fpc= -6.0, fpcu= -5.0, epscu= -0.014)
unconfinedConcrete= typical_materials.defConcrete01(preprocessor, 'unconfinedConcrete', epsc0= -0.002, fpc= -5.0, fpcu= -0.0, epscu= -0.006)
## Reinforcing steel
reinforcingSteel= typical_materials.defSteel01(preprocessor, 'reinforcingSteel', E= 30000.0, fy= 60.0, b= .01)

# Define reinforced concrete section.
colWidth= 15
colDepth= 24

concreteCover= 1.5
As= 0.6 # area of no. 7 bars

y1= colDepth/2.0
z1= colWidth/2.0

materialHandler= preprocessor.getMaterialHandler
fiberSection= materialHandler.newMaterial("fiber_section_2d","fiberSection")
fiberSectionRepr= fiberSection.getFiberSectionRepr()
sectionGeometry= preprocessor.getMaterialHandler.newSectionGeometry("sectionGeometry")
regions= sectionGeometry.getRegions

# Create the concrete core region.
confinedConcreteRegion= patch(regions= regions, material= confinedConcrete, numSubdivY= 10, numSubdivZ= 1, yI= concreteCover-y1, zI= concreteCover-z1, yJ= y1-concreteCover, zJ= z1-concreteCover)

# Create the concrete cover regions.
unconfinedConcreteRegionA= patch(regions= regions, material= unconfinedConcrete, numSubdivY= 10, numSubdivZ= 1, yI=-y1, zI= z1-concreteCover, yJ= y1, zJ= z1)
unconfinedConcreteRegionB= patch(regions= regions, material= unconfinedConcrete, numSubdivY= 10, numSubdivZ= 1, yI=-y1, zI= -z1, yJ= y1, zJ= concreteCover-z1)
unconfinedConcreteRegionC= patch(regions= regions, material= unconfinedConcrete, numSubdivY= 2, numSubdivZ= 1, yI= -y1, zI= concreteCover-z1, yJ= concreteCover-y1, zJ= z1-concreteCover)
unconfinedConcreteRegionD= patch(regions= regions, material= unconfinedConcrete, numSubdivY= 2, numSubdivZ= 1, yI= y1-concreteCover, zI= concreteCover-z1, yJ= y1, zJ= z1-concreteCover)

# Create the reinforcing fibers (left, middle, right)
reinforcement= sectionGeometry.getReinfLayers
reinforcementLeft= reinforcement.newStraightReinfLayer(reinforcingSteel.name)
reinforcementLeft.numReinfBars= 3
reinforcementLeft.barArea= As
reinforcementLeft.p1= geom.Pos2d(y1-concreteCover, z1-concreteCover)
reinforcementLeft.p2= geom.Pos2d(y1-concreteCover, concreteCover-z1)
reinforcementMiddle= reinforcement.newStraightReinfLayer(reinforcingSteel.name)
reinforcementMiddle.numReinfBars= 2
reinforcementMiddle.barArea= As
reinforcementMiddle.p1= geom.Pos2d(0.0,z1-concreteCover)
reinforcementMiddle.p2= geom.Pos2d(0.0, concreteCover-z1)
reinforcementRight= reinforcement.newStraightReinfLayer(reinforcingSteel.name)
reinforcementRight.numReinfBars= 3
reinforcementRight.barArea= As
reinforcementRight.p1= geom.Pos2d(concreteCover-y1, z1-concreteCover)
reinforcementRight.p2= geom.Pos2d(concreteCover-y1, concreteCover-z1)
fiberSectionRepr.setGeomNamed(sectionGeometry.name)
fiberSection.setupFibers()

# Estimate yield curvature
# (Assuming no axial load and only top and bottom steel)
d= colDepth-concreteCover # d -- from cover to rebar
epsy= reinforcingSteel.fy/reinforcingSteel.E # steel yield strain
Ky= epsy/(0.7*d)

print( "Estimated yield curvature: ", Ky)

# Set axial load 
P= -180

mu= 15 # Target ductility for analysis
numIncr= 100 # Number of analysis increments

modelSpace.ti= list()
modelSpace.ky= list()
modelSpace.mi= list()
moment_curvature(modelSpace, fiberSection, P, Ky*mu, numIncr)

'''
print(modelSpace.ti)
print(modelSpace.ky)
print(modelSpace.mi)
'''

# Display Matplotlib graphics.
import matplotlib.pyplot as plt
plot_diagram(plt, modelSpace.ky, modelSpace.mi)

# Section output
fig = plt.figure()
ax= fig.add_subplot(111)
plot_fiber_section.mplot_section_geometry(ax, sectionGeometry= sectionGeometry)
plt.show()
