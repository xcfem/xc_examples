# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import geom
import xc

from materials.ehe import EHE_materials
from materials.sections.fiber_section import fiber_sets
from model import predefined_spaces
from solution import predefined_solutions

import geom_I_beam as gbeam
import data_beam_type2 as dat


# design bending moment and axial force
MyDato= 6230e3   # vigas centrales con luz 
NDato= 0.0
Acordon=140e-6 # área del cordon
NroturaCordon=260e3 #carga de rotura del cordon
PinitCordon=0.75*NroturaCordon # pretensado inicial
sigmaPinit=PinitCordon/Acordon # tensión pretensado incial
losses=0.20
sigmaPinit_calc=(1-losses)*sigmaPinit # tensión pretensado incial a efectos de cálculo

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
concrete= EHE_materials.HP55
activeSteel=EHE_materials.Y1860S7
passiveSteel=EHE_materials.B500S

# Materials definition (diagrams)
concreteDiag= concrete.defDiagD(preprocessor)
# activeSteelDiag= activeSteel.defDiagD(preprocessor, EHE_materials.Y1860S7.tInic())
activeSteelDiag=activeSteel.defDiagD(preprocessor, sigmaPinit_calc)
passiveSteelDiag= passiveSteel.defDiagD(preprocessor)

# Create RC section model.
geomSecPret=gbeam.gmSecHP_viga_jabali(preprocessor, "prestressedConcretSectionGeom",concrete.nmbDiagD,passiveSteel.nmbDiagD,activeSteel.nmbDiagD,dat.concreteLstWidthHeight,dat.activeReinLayers,dat.passiveReinLayers,zStart=-1.5/2)

# 

materialHandler= preprocessor.getMaterialHandler
secHP= materialHandler.newMaterial("fiber_section_3d","secHP")
fiberSectionRepr= secHP.getFiberSectionRepr()
fiberSectionRepr.setGeomNamed(geomSecPret.name)
secHP.setupFibers()
'''
print('Area sección fibras= ', secHP.getArea())
print('Iz= ',secHP.EIz()/EHE_materials.HP55.Ecm())
print('Iy= ',secHP.EIy()/EHE_materials.HP55.Ecm())
print('I1= ',secHP.getEI1()/EHE_materials.HP55.Ecm())
print('I2= ',secHP.getEI2()/EHE_materials.HP55.Ecm())
'''

nodes= preprocessor.getNodeHandler

modelSpace= predefined_spaces.StructuralMechanics3D(nodes)
# nodA= nodes.newNodeXYZ(1,0,0)
# nodB= nodes.newNodeXYZ(1,0,0)
nodA= nodes.newNodeXYZ(1,0,0)
nodB= nodes.newNodeXYZ(1,0,0)

elementos= preprocessor.getElementHandler
elementos.dimElem= 1
elementos.defaultMaterial= "secHP"
zlElement= elementos.newElement("ZeroLengthSection",xc.ID([nodA.tag,nodB.tag]))
#elem= zlElement, nodA, nodB= sectionModel(preprocessor, "secHP")

# Constraints
modelSpace= predefined_spaces.getStructuralMechanics3DSpace(preprocessor)
modelSpace.fixNode000_000(nodA.tag)
#modelSpace.fixNodeF00_00F(nodB.tag)
modelSpace.fixNodeF00_0FF(nodB.tag)

# Loads definition
lp0= modelSpace.newLoadPattern(name= '0')
lp0.newNodalLoad(nodB.tag,xc.Vector([NDato,0,0,0,-MyDato,0]))

# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp0.name)

# Solution procedure
solProc= predefined_solutions.PlainNewtonRaphson(feProblem, maxNumIter=100, convergenceTestTol= 1e-2, printFlag=True)
analOk= solProc.solve(calculateNodalReactions= True, reactionCheckTolerance= 1e-3)

# Results
RN= nodA.getReaction[0] 
RM= nodA.getReaction[5] 
RN2= nodB.getReaction[0] 
sccEl1= zlElement.getSection()
esfN= sccEl1.getStressResultantComponent("N")
esfMy= sccEl1.getStressResultantComponent("My")
print('My=', round(esfMy*1e-3,0),' kNm')
esfMz= sccEl1.getStressResultantComponent("Mz")
defMz= sccEl1.getSectionDeformationByName("defMz")
defN= sccEl1.getSectionDeformationByName("defN")
concrFibers= fiber_sets.FiberSet(sccEl1,'concreteFiberSet',concrete.matTagD)
fibraCEpsMin= concrFibers.getFiberWithMinStrain()
epsCMin= fibraCEpsMin.getMaterial().getStrain() # Minimum concrete strain
sigmaCMin=fibraCEpsMin.getMaterial().getStress() # Minimum concrete stress
print('Pto. ',fibraCEpsMin.getPos(), '; -Minimum concrete strain=', round(epsCMin*1e3,1), ' por mil;  -Minimum concrete stress=', round(sigmaCMin*1e-6,2), ' MPa')
yEpsCMin= fibraCEpsMin.getPos().x
fibraCEpsMax= concrFibers.getFiberWithMaxStrain()
epsCMax= fibraCEpsMax.getMaterial().getStrain() # Maximum concrete strain.
sigmaCMax=fibraCEpsMax.getMaterial().getStress()
print('Pto. ',fibraCEpsMax.getPos(), '; -Maximum concrete strain=', round(epsCMax*1e3,1), ' por mil;  -Maximum concrete stress=', round(sigmaCMax*1e-6,2), ' MPa')
activeReinfFibers= fiber_sets.FiberSet(sccEl1,"active reinforcement",activeSteel.matTagD)
fibraActSEpsMax= activeReinfFibers.getFiberWithMaxStrain()
epsActSMax= fibraActSEpsMax.getMaterial().getStrain() # Maximum active steel strain
sigmaActSMax= fibraActSEpsMax.getMaterial().getStress() # Maximum active steel strain
print('Pto. ',fibraActSEpsMax.getPos(), '; -Maximum active-steel strain=', round(epsActSMax*1e3,1), ' por mil;  -Maximum active-steel stress=', round(sigmaActSMax*1e-6,2), ' MPa')
activeReinfFibers= fiber_sets.FiberSet(sccEl1,"active reinforcement",activeSteel.matTagD)
fibraActSEpsMin= activeReinfFibers.getFiberWithMinStrain()
epsActSMin= fibraActSEpsMin.getMaterial().getStrain() # Minimum active steel strain
sigmaActSMin= fibraActSEpsMin.getMaterial().getStress() # Minimum active steel strain
print('Pto. ',fibraActSEpsMin.getPos(), '; -Minimum active-steel strain=', round(epsActSMin*1e3,1), ' por mil;  -Minimum active-steel stress=', round(sigmaActSMin*1e-6,2), ' MPa')

passiveReinfFibers= fiber_sets.FiberSet(sccEl1,"passive reinforcement",passiveSteel.matTagD)
fibraPasSEpsMax= passiveReinfFibers.getFiberWithMaxStrain()
epsPasSMax= fibraPasSEpsMax.getMaterial().getStrain() # Maximum passive steel strain
sigmaPasSMax= fibraPasSEpsMax.getMaterial().getStress() # Maximum passive steel strain
print('Pto. ',fibraPasSEpsMax.getPos(), '; -Maximum passive-steel strain=', round(epsPasSMax*1e3,1), ' por mil;  -Maximum passive-steel stress=', round(sigmaPasSMax*1e-6,2), ' MPa')


passiveReinfFibers= fiber_sets.FiberSet(sccEl1,"passive reinforcement",passiveSteel.matTagD)
fibraPasSEpsMin= passiveReinfFibers.getFiberWithMinStrain()
epsPasSMin= fibraPasSEpsMin.getMaterial().getStrain() # Minimum passive steel strain
sigmaPasSMin= fibraPasSEpsMin.getMaterial().getStress() # Minimum passive steel strain
print('Pto. ',fibraPasSEpsMin.getPos(), '; -Minimum passive-steel strain=', round(epsPasSMin*1e3,1), ' por mil;  -Minimum passive-steel stress=', round(sigmaPasSMin*1e-6,2), ' MPa')



from materials.sections import section_properties
from materials.ehe import EHE_limit_state_checking
solicitationType= section_properties.solicitationType(epsCMin,epsPasSMax)
solicitationTypeString= section_properties.solicitationTypeString(solicitationType)
cumpleFT= EHE_materials.ReinforcedConcreteLimitStrainsEHE08.bendingOK(epsCMin,epsPasSMax)
aprovSecc= EHE_materials.ReinforcedConcreteLimitStrainsEHE08.getBendingEfficiency(epsCMin,epsPasSMax)

print('Section capacity factor=',aprovSecc)

# # plot cross-section strains and stresses 
from postprocess import utils_display
# '''
#   fiberSet: set of fibers to be represented
#   title:    general title for the graphic
#   fileName: name of the graphic file (defaults to None: no file generated)
#   nContours: number of contours to be generated (defaults to 100)
# '''
utils_display.plotStressStrainFibSet(fiberSet=concrFibers.fSet,title='cross-section concrete fibers',fileName='concrete.jpeg',nContours=0)
utils_display.plotStressStrainFibSet(fiberSet=activeReinfFibers.fSet,title='cross-section active steel fibers',fileName='active_steel.jpeg',nContours=0)
utils_display.plotStressStrainFibSet(fiberSet=passiveReinfFibers.fSet,title='cross-section passive steel fibers',fileName='passive_steel.jpeg',nContours=0)


quit()


f
'''
from materials.sections.fiber_section import plot_fiber_section as pfs
fsPlot= pfs.FibSectFeaturesToplot(fiberSection=secHP)
fsPlot.colorNeutralAxis ='r'
fsPlot.colorBendingPlane ='g'
fsPlot.colorCompressionPlane ='b'
fsPlot.colorTensionPlane ='m'
fsPlot.colorIntForcAxis ='c'
fsPlot.colorLeverArm ='orange'
fsPlot.colorEffDepth ='purple'
fsPlot.colorEffConcrArea ='brown'
fsPlot.MaxEffHeight = heffmax_EC2
fsPlot.colorGrossEffConcrAreaContours ='m'
fig1,ax2d=fsPlot.generatePlot()
fig1.show()
fig1.savefig('fig1.png')
'''

