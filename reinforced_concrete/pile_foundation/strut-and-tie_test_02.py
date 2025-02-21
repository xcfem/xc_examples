# -*- coding: utf-8 -*-
''' Not so naive approach to calculation of pile cap on two piles. Home made test.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis Claudio Pérez Tato (LCPT)"
__copyright__= "Copyright 2025, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import xc
from model import predefined_spaces
from materials.ec2 import EC2_materials
from materials.sections.fiber_section import def_simple_RC_section
from materials.sections.fiber_section import def_column_RC_section
from misc_utils import log_messages as lmsg
from solution import predefined_solutions
import strut_and_tie_utils

# Problem type.
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Problem geometry.
#    
#                n0
#                 |  pier
#                 |
#       n1   n2   |n3 n4   n5
#         +----+--+--+----+
#         | \ /.\  / .\  /|
#         |  / .  \  . \/ |  d
#         | / \./   \. / \|
#         +----+-----+----+
#       n6|   n7     n8   |n9
#         |               | 
#         |               | pile
#         |               |
#        n10             n11
#    
s= 1.6
d= 1.0
pierHeight= 2
pileLength= 5.0
pierSide= 0.25
pileDiameter= 150e-3
v= s/2.0
a= pierSide/2.0

## Define mesh.
### Top of the pier.
n0= modelSpace.newNode(0.0, d+pierHeight) # pier top.
n3= modelSpace.newNode(0.0, d) # pier bottom.
### Bottom of the abutment.
n6= modelSpace.newNode(-v, 0.0) # left pile top.
n9= modelSpace.newNode(v, 0.0) # right pile top.
### Bottom of the piles.
n10= modelSpace.newNode(-v, -pileLength)
n11= modelSpace.newNode(v, -pileLength)

pilecap= strut_and_tie_utils.Pilecap2Piles(pierBottomNode= n3, leftPileTopNode= n6, rightPileTopNode= n9, pierEffectiveWidth= pierSide)

# Define materials. 
concrete= EC2_materials.C30
strutArea= 0.25
reinfSteel= EC2_materials.S500B
tieArea= 5.8e-4
## Define pier material.
pierRCSection= def_simple_RC_section.RCRectangularSection(name= 'pierRCSection', sectionDescr= 'pier section', concrType= concrete, reinfSteelType= reinfSteel, width= pierSide, depth= pierSide)
xcPierSectionMaterial= pierRCSection.defElasticShearSection2d(preprocessor)

# Define pile cap.
pilecap.createStrutAndTieModel(modelSpace, strutArea= strutArea, concrete= concrete, topDownTiesArea= tieArea, bottomChordTiesArea= tieArea, topChordTiesArea= tieArea, reinfSteel= reinfSteel, xcPierSectionMaterial= xcPierSectionMaterial)

### Define pier.
#### Define pier elements.
lin= modelSpace.newLinearCrdTransf("lin")
modelSpace.setDefaultCoordTransf(lin)
modelSpace.setDefaultMaterial(xcPierSectionMaterial)
modelSpace.newElement('ElasticBeam2d', [n0.tag, n3.tag])

### Define piles.
#### Define pile material.
pilesRCSection= def_column_RC_section.RCCircularSection(name= 'pilesRCSection', sectionDescr= 'piles section', concrType= concrete, reinfSteelType= reinfSteel, Rext= pileDiameter/2.0)
pilesMaterial= pilesRCSection.defElasticShearSection2d(preprocessor, reductionFactor= 1.0)
modelSpace.setDefaultMaterial(pilesMaterial)
modelSpace.newElement('ElasticBeam2d', [n6.tag, n10.tag])
modelSpace.newElement('ElasticBeam2d', [n9.tag, n11.tag])

## Define constraints
modelSpace.fixNode('000', n10.tag)
modelSpace.fixNode('000', n11.tag)

# Load definition.
F= 1.5*183e3
lp0= modelSpace.newLoadPattern(name= '0')
lp0.newNodalLoad(n0.tag,xc.Vector([0,-F,0]))
# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp0.name)

# Solution
analysis= predefined_solutions.penalty_newton_raphson(feProblem, printFlag= 1)
result= analysis.analyze(1)
if(result!=0):
    lmsg.error("Can't solve.")
    info= None
    solver= analysis.linearSOE.solver
    if(solver.hasProp("info")):
        info= solver.getProp("info")
    unconstrainedNode= modelSpace.locateEquationNumber(eqNumber= info-1)
    print('unconstrained node id: ', unconstrainedNode.tag)
    print('unconstrained node position: ', unconstrainedNode.getInitialPos2d)
    # exit(1)

'''
# Check results.
T0= (tie67.getN()+tie89.getN())/2.0
T0ref= F*(v-a)/2.0/d
ratio1= abs(T0-T0ref)/T0ref

modelSpace.removeLoadCaseFromDomain(lp0.name)
modelSpace.revertToStart()
lp1= modelSpace.newLoadPattern(name= '1')
lp1.newNodalLoad(n0.tag,xc.Vector([F,0,0]))
# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp1.name)

result= analysis.analyze(1)
if(result!=0):
    lmsg.error("Can't solve.")
    exit(1)
    
modelSpace.removeLoadCaseFromDomain(lp1.name)
modelSpace.revertToStart()
lp2= modelSpace.newLoadPattern(name= '2')
lp2.newNodalLoad(n0.tag,xc.Vector([0,F,0]))
# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp2.name)

result= analysis.analyze(1)
if(result!=0):
    lmsg.error("Can't solve.")
    exit(1)
    
modelSpace.removeLoadCaseFromDomain(lp2.name)
modelSpace.revertToStart()
lp3= modelSpace.newLoadPattern(name= '3')
lp3.newNodalLoad(n0.tag,xc.Vector([F,F,0]))
# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp3.name)

result= analysis.analyze(1)
if(result!=0):
    lmsg.error("Can't solve.")
    exit(1)

# print('dummy12.N= ', dummy12.getN()/1e3)
# print('dummy45.N= ', dummy45.getN()/1e3)
# print('dummy78.N= ', dummy78.getN()/1e3)
# print('\ntie12.N= ', tie67.getN()/1e3)
# print('tie89.N= ', tie89.getN()/1e3)
print('T0= ', T0/1e3, 'kN')
print('T0ref= ', T0ref/1e3, 'kN')
print('ratio1= ', ratio1)

import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if abs(ratio1)<1e-3:
    print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
'''

# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)
# oh.displayBlocks()
oh.displayFEMesh()
oh.displayLoads()
oh.displayReactions()
oh.displayIntForcDiag('N')
# oh.displayDispRot(itemToDisp='uY')

