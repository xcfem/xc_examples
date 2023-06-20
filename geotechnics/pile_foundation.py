# -*- coding: utf-8 -*-
import math
import geom
import xc
from model import predefined_spaces
from materials.ehe import EHE_materials
from materials import typical_materials as tm
from materials.sections import section_properties as sectpr
from model.geometry import  pile_foundation as pilefound
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl

#    ***   Data   ****
#Pile cap data
Hpilecap=1.5 #pile-cap height [m]
Apilecap=5.5*5.5 #Area of the pile-cap base [m2]
Hfill_pilecap=4.0-Hpilecap  #height of earth filling over pile-cap
fill_dens=2e3   #density of earth filling [kg/m3]
#Ground data
zGround=Hpilecap+Hfill_pilecap

##Pile data
#nXpile=2 #number of piles in X direction
distXpile=3 #distance between piles in X direction
#nYpile=2 #number of piles in Y direction
distYpile=3 #distance between piles in Y direction
pileDiam=1  #pile diameter
pileLenght=14   #pile length
pileType='endBearing' #type of pile 'endBearing' or 'friction'
soils=[(zGround-3.0,'clay',15e6/75),(zGround-17.0,'clay',120e6/75),(zGround-100,'clay',275e6/75)]
#Properties of the clay soils
# soils [(zBottom,type, su), ...]  where 'zBottom' is the global Z coordinate
#           of the bottom level of the soil and 'su' [Pa/m] is the
#           shear strength of the saturated cohesive soil [Pa/m]
#           su=constante rigidez horizontal [N/m] / 75

pileConcr=EHE_materials.HA30  #pile concrete
LeqPile=round(math.pi**0.5*pileDiam/2.,3)
bearingCapPile=3903e3 #total bearing capacity of the pile [N]

eSize=0.5 # pile-elements size

# *******
FEcase= xc.FEProblem()
prep=FEcase.getPreprocessor
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) #Defines the
# dimension of the space: nodes by three coordinates (x,y,z) and 
# six DOF for each node (Ux,Uy,Uz,thetaX,thetaY,thetaZ)
sty=outSty.OutputStyle() 
sty.language='en'
out=outHndl.OutputHandler(modelSpace,sty)

# Pile material and section
pileConcrProp=tm.MaterialData(name='pileConcrProp',E=pileConcr.Ecm(),nu=pileConcr.nuc,rho=pileConcr.density())
geomSectPile=sectpr.RectangularSection(name='geomSectPile',b=LeqPile,h=LeqPile)
pile_mat=tm.BeamMaterialData(name='pile_mat', section=geomSectPile, material=pileConcrProp)
pile_mat.setupElasticShear3DSection(preprocessor=prep)
piles=prep.getSets.defSet('piles')

# 1 column, 4 piles
n1=nodes.newNodeXYZ(0,0,0)
(struts1,ties1,topNodPiles1)=pilefound.gen_pile_cap_1column_4piles(
    modelSpace=modelSpace,
    nodCol=n1,
    distXpile=distXpile,
    distYpile=distYpile,
    Hpilecap=Hpilecap,
    nameSetStruts='struts1',
    nameSetTies='ties1')
piles1=pilefound.gen_piles(
    modelSpace=modelSpace,
    topNodPiles=topNodPiles1,
    pileDiam=pileDiam,
    pileLenght=pileLenght,
    pileMat=pile_mat,
    eSize=eSize,
    pileType=pileType,
    bearingCapPile=bearingCapPile,
    soils=soils,
    nameSetPiles='piles1',
    alphaK=[1,1,1])


# N columns, Nx2 piles
y=5
distCols=1.5
nodCols=[nodes.newNodeXYZ(-2*distCols,y,0),
         nodes.newNodeXYZ(-distCols,y,0),
         nodes.newNodeXYZ(0,y,0),
         nodes.newNodeXYZ(distCols,y,0),
         nodes.newNodeXYZ(2*distCols,y,0),
         ]

(struts2,ties2,topNodPiles2)=pilefound.gen_pile_cap_Ncolumns_Nx2_piles(
    modelSpace=modelSpace,
    nodCols=nodCols,
    distXpile=distXpile,
    distYpile=distYpile,
    Hpilecap=Hpilecap,
    nameSetStruts='struts2',
    nameSetTies='ties2')
piles2=pilefound.gen_piles(
    modelSpace=modelSpace,
    topNodPiles=topNodPiles2,
    pileDiam=pileDiam,
    pileLenght=pileLenght,
    pileMat=pile_mat,
    eSize=eSize,
    pileType=pileType,
    bearingCapPile=bearingCapPile,
    soils=soils,
    nameSetPiles='piles2',
    alphaK=[1,1,1])
        
# 2 columns, 4 piles
y=10
distCols=2
nodCols=[nodes.newNodeXYZ(-distCols/2,y,0),
         nodes.newNodeXYZ(distCols/2,y,0)]
distXpile=4
(struts3,ties3,topNodPiles3)=pilefound.gen_pile_cap_2columns_4piles(
    modelSpace=modelSpace,
    nodCols=nodCols,
    distXpile=distXpile,
    distYpile=distYpile,
    Hpilecap=Hpilecap,
    nameSetStruts='struts3',
    nameSetTies='ties3')
piles3=pilefound.gen_piles(
    modelSpace=modelSpace,
    topNodPiles=topNodPiles3,
    pileDiam=pileDiam,
    pileLenght=pileLenght,
    pileMat=pile_mat,
    eSize=eSize,
    pileType=pileType,
    bearingCapPile=bearingCapPile,
    soils=soils,
    nameSetPiles='piles3',
    alphaK=[1,1,1])
        

# 2 columns, 3X-2Y piles
y=18
distCols=3
nodCols=[nodes.newNodeXYZ(-distCols/2,y,0),
         nodes.newNodeXYZ(distCols/2,y,0)]
distXpile=4
distYpile=5
(struts4,ties4,topNodPiles4)=pilefound.gen_pile_cap_2columns_3X2Ypiles(
    modelSpace=modelSpace,
    nodCols=nodCols,
    distXpile=distXpile,
    distYpile=distYpile,
    Hpilecap=Hpilecap,
    nameSetStruts='struts4',
    nameSetTies='ties4')
piles4=pilefound.gen_piles(
    modelSpace=modelSpace,
    topNodPiles=topNodPiles4,
    pileDiam=pileDiam,
    pileLenght=pileLenght,
    pileMat=pile_mat,
    eSize=eSize,
    pileType=pileType,
    bearingCapPile=bearingCapPile,
    soils=soils,
    nameSetPiles='piles4',
    alphaK=[1,1,1])
        



out.displayFEMesh()
