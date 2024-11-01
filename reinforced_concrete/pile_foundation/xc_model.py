# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
import math
import geom
import xc
from model import predefined_spaces
from materials import typical_materials
from materials.ehe import EHE_materials
from actions import loads
from actions import load_cases as lcases
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl
sty=outSty.OutputStyle() 
#out=outHndl.OutputHandler(modelSpace,sty)
sty.language='es'

# local functions
import pile_foundation_funct as pilfound

######

FEcase= xc.FEProblem()
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) #Defines the
out=outHndl.OutputHandler(modelSpace,sty)
concrete=EHE_materials.HA30
steel=EHE_materials.B500S

# Data column
nodCol=nodes.newNodeXYZ(0,0,0)
nodTopCol=nodes.newNodeXYZ(0,0,0.5)
# Data reinforcement
tieRebFi=25e-3
nTieReb=13
areaTie=nTieReb*math.pi*tieRebFi**2/4
# Data piles
nRows=4 # number of pile rows (in X direction)
distXpile=4
distYpile=5
pileDiam=1.0
pileLenght=14
zGround=0
soils=[(zGround-4.0,'clay',15e6/75),(zGround-8.5,'clay',30e6/75),(zGround-100,'clay',120e6/75)]
bearingCapPile=3806e3 #total bearing capacity of the pile [N]
eSizePiles=0.5
pileType='endBearing'
#  Data pilecap
Hpilecap=1.5
# Data beam
Lbeam=nRows*distXpile
esizeBeam=0.25
wBeam=0.1#1.0
hBeam=0.1#10.0
#Data struts
areaStrut=0.5
# End data
# Column 
from materials.sections import section_properties as sectpr
## column foundation
concrProp=typical_materials.MaterialData(name='concrProp',E=concrete.Ecm(),nu=concrete.nuc,rho=concrete.density())
geomSectPile=sectpr.CircularSection(name='geomSectPile',Rext=pileDiam/2)
pileMat=typical_materials.BeamMaterialData(name='pileMat', section=geomSectPile, material=concrProp)
pileMat.setupElasticShear3DSection(preprocessor=prep)
strutsCol,tiesCol,topNodPilesCol=pilfound.gen_pile_cap_1column_4piles(modelSpace,concrete,steel,nodCol,LxFictCol=0.4,LyFictCol=0.4,areaFictCol=1,distXpile=distXpile,distYpile=distYpile,Hpilecap=Hpilecap,areaStrut=areaStrut,areaTie=areaTie,nameSetStruts='strutsCol',nameSetTies='tiesCols',nameSetFbeams='setFbeamsCol')
pilesCol=pilfound.gen_piles(modelSpace,topNodPilesCol,pileDiam,pileLenght,pileMat,eSizePiles,pileType,bearingCapPile,soils,nameSetPiles='pilesCol',alphaK=[1,1,1])
## column
elements.defaultMaterial=pileMat.name
linX= modelSpace.newLinearCrdTransf("linX",xc.Vector([1,0,0]))
elements.defaultTransformation=linX.name
column=elements.newElement("ElasticBeam3d",xc.ID([nodCol.tag,nodTopCol.tag]))

# Beam (abutment)
yBeam=-5
beamAbut=prep.getSets.defSet('beam')
nodBeam=[nodes.newNodeXYZ(x,yBeam,0) for x in [esizeBeam*i for i in range(0,int(Lbeam/esizeBeam)+1)]]
geomSectBeam=sectpr.RectangularSection('geomSectBeam',wBeam,hBeam)
beamMat=typical_materials.BeamMaterialData(name='beamMat', section=geomSectBeam, material=concrProp)
beamMat.setupElasticShear3DSection(prep)
elements.defaultMaterial=pileMat.name
linZ=modelSpace.newLinearCrdTransf("linZ",xc.Vector([0,0,1]))
elements.defaultTransformation=linZ.name
for i in range(len(nodBeam)-1):
    e=elements.newElement("ElasticBeam3d",xc.ID([nodBeam[i].tag,nodBeam[i+1].tag]))
    beamAbut.elements.append(e)
beamAbut.fillDownwards()
xCentBeam=Lbeam/2
x=xCentBeam-(nRows-1)*distXpile/2+distXpile/2#distXpile/2
nCol1=beamAbut.nodes.getNearestNode(geom.Pos3d(x,yBeam,0))
x+=distXpile                                   
nCol2=beamAbut.nodes.getNearestNode(geom.Pos3d(x,yBeam,0))
x+=distXpile                                 
nCol3=beamAbut.nodes.getNearestNode(geom.Pos3d(x,yBeam,0))
nodColsAbut=[nCol1,nCol2,nCol3]

strutsAbut,tiesAbut,topNodPilesAbut=pilfound.gen_pile_cap_Ncolumns_Nplus1x2_piles(modelSpace,concrete,steel,nodCols=nodColsAbut,LxFictCol=0.4,LyFictCol=0.4,areaFictCol=1,distXpile=distXpile,distYpile=distYpile,Hpilecap=Hpilecap,areaStrut=areaStrut,areaTie=areaTie,nameSetStruts='strutsAbut',nameSetTies='tiesAbuts',nameSetFbeams='setFbeamsAbut')
pilesAbut=pilfound.gen_piles(modelSpace,topNodPilesAbut,pileDiam,pileLenght,pileMat,eSizePiles,pileType,bearingCapPile,soils,nameSetPiles='pilesAbut',alphaK=[1,1,1])
'''
elements.defaultMaterial='matStrut'
strut1=elements.newElement("Truss",xc.ID([topNodPilesAbut[0].tag,nodBeam[0].tag]))
strut2=elements.newElement("Truss",xc.ID([topNodPilesAbut[1].tag,nodBeam[0].tag]))
strut3=elements.newElement("Truss",xc.ID([topNodPilesAbut[-1].tag,nodBeam[-1].tag]))
strut4=elements.newElement("Truss",xc.ID([topNodPilesAbut[-2].tag,nodBeam[-1].tag]))
for e in [strut1,strut2,strut3,strut4]:
        e.sectionArea=areaStrut
        strutsAbut.getElements.append(e)
'''
out.displayFEMesh([strutsCol,tiesCol,pilesCol,beamAbut,strutsAbut,tiesAbut,pilesAbut])

# Load cases
vloadCol=xc.Vector([0,0,-10e3,0,0,0])
vloadNBeam=vloadCol/len(nodBeam)                  

LC01=lcases.LoadCase(preprocessor=prep,name='LC01',loadPType="default",timeSType="constant_ts")
LC01.create()
nodTopCol.newLoad(vloadCol)
for n in nodBeam:
    n.newLoad(vloadNBeam)
modelSpace.removeAllLoadPatternsFromDomain()
modelSpace.addLoadCaseToDomain(LC01.name)

out.displayLoads(beamAbut)

from solution import predefined_solutions
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')
'''
out.displayIntForcDiag('N',pilesCol)
out.displayIntForcDiag('Vy',pilesCol)
out.displayIntForcDiag('Vz',pilesCol)
out.displayIntForcDiag('My',pilesCol)
out.displayIntForcDiag('Mz',pilesCol)
out.displayIntForcDiag('N',strutsCol)
out.displayIntForcDiag('N',tiesCol)
'''

out.displayIntForcDiag('N',pilesAbut)
out.displayIntForcDiag('Vy',pilesAbut)
out.displayIntForcDiag('Vz',pilesAbut)
out.displayIntForcDiag('My',pilesAbut)
out.displayIntForcDiag('Mz',pilesAbut)

out.displayIntForcDiag('N',strutsAbut)
out.displayIntForcDiag('N',tiesAbut)


