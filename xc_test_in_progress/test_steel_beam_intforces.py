# -*- coding: utf-8 -*-
from __future__ import print_function
__author__= "Ana Ortega (AO_O)"
__copyright__= "Copyright 2018, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "ana.ortega@ciccp.es"

import geom
import xc
from materials.ec3 import EC3_materials
from model.geometry import grid_model as gm
from model.mesh import finit_el_model as fem
from model import predefined_spaces
from materials.ec3 import EC3Beam as ec3b
from materials.ec3 import EC3_limit_state_checking as EC3lsc
from actions import loads
from actions import load_cases as lcases
from actions import combinations as comb
from postprocess.config import default_config
from postprocess import limit_state_data as lsd

cfg=default_config.EnvConfig(language='sp', resultsPath= 'tmp_results/', intForcPath= 'internalForces/',verifPath= 'verifications/')

FEcase= xc.FEProblem()
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) #Defines the
# dimension of the space: nodes by three coordinates (x,y,z) and 
# six DOF for each node (Ux,Uy,Uz,thetaX,thetaY,thetaZ)

# coordinates in global X,Y,Z axes for the grid generation
xList=[0]
yList=[0,1,3,6,7]
zList=[0]
lastYpos=len(yList)-1

eSize= 0.2     #length of elements

# grid model definition
gridGeom= gm.GridModel(prep,xList,yList,zList)

# Grid geometric entities definition (points, lines, surfaces)
# Points' generation
gridGeom.generatePoints()

gridGeom.movePointsRange(gm.IJKRange((0,1,0),(0,1,0)),xc.Vector([0.0,0,1.0]))
gridGeom.movePointsRange(gm.IJKRange((0,2,0),(0,3,0)),xc.Vector([0.0,0,1.5]))

beamY_rg=gm.IJKRange((0,0,0),(0,lastYpos,0))
beamY=gridGeom.genLinOneRegion(ijkRange=beamY_rg,setName='beamY')
#                         *** MATERIALS *** 
S235JR= EC3_materials.S235JR
S235JR.gammaM= 1.00


# Steel material-section appropriate for 3D beam analysis, including shear
  # deformations.
  # Attributes:
  #   steel:         steel material (
  #   name: name of the standard steel profile. Types: IPEShape, HEShape,
  #         UPNShape, AUShape, CHSShape
  #      (defined in materials.sections.structural_shapes.arcelor_metric_shapes)
beamY_mat= EC3_materials.IPEShape(steel=S235JR,name='IPE_A_450')
beamY_mat.sectionClass= beamY_mat.getClassInBending()
beamY_mat.defElasticShearSection3d(preprocessor)

#                         ***FE model - MESH***

beamY_mesh=fem.LinSetToMesh(linSet=beamY,matSect=beamY_mat,elemSize=eSize,vDirLAxZ=xc.Vector([1,0,0]),elemType='ElasticBeam3d',coordTransfType='linear')
beamY_mesh.generateMesh(preprocessor)
# boundary conditions
p1=gridGeom.getPntGrid([0,0,0])
modelSpace.fixNode000_FFF(p1.getNode().tag)
p2=gridGeom.getPntGrid([0,4,0])
modelSpace.fixNode000_FFF(p2.getNode().tag)

# Loads and combinations
qunif=loads.UniformLoadOnBeams(name='qunif', xcSet=beamY, loadVector=xc.Vector([0,0,-1e3,0,0,0]),refSystem='Global')

LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([qunif])

combContainer= comb.CombContainer()
combContainer.ULS.perm.add('ELU01', '1.2*LC1')

# EC3beam definition
# Support coefficients (1==free, 0.5==prevented) (all default to 1)
# ky: lateral bending, kw: warping, k1: warping and lateral bending at left
# end, k2:  warping and lateral bending at right end
supCf_free=EC3lsc.BeamSupportCoefficients(ky=1.0,kw=1.0,k1=1.0,k2=1.0)
supCf=EC3lsc.BeamSupportCoefficients(ky=1.0,kw=1.0,k1=0.5,k2=1.0)

lstLines=gridGeom.getLstLinRange(beamY_rg)

ec3beam= ec3b.EC3Beam(name='ec3bm',ec3Shape=beamY_mat, beamSupportCoefs=supCf_free,lstLines=lstLines)
ec3beam.setControlPoints()
ec3beam.installULSControlRecorder(recorderType="element_prop_recorder")

# Internal forces calculation
limitStates= [lsd.steelNormalStressesResistance]
lsd.steelNormalStressesResistance.envConfig=cfg
for ls in limitStates:
    ls.saveAll(combContainer,setCalc=beamY)

# Graphic stuff    
# Default configuration of environment variables.
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl
sty=outSty.OutputStyle() 
out=outHndl.OutputHandler(modelSpace,sty)
modelSpace.addLoadCaseToDomain('LC1')
from solution import predefined_solutions
analysis= predefined_solutions.simple_static_linear(FEcase)
result= analysis.analyze(1)
out.displayDispRot('uZ')

