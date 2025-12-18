# import local modules
from solution import predefined_solutions

from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
# Common variables
out=xc_init.out
modelSpace=xc_init.modelSpace
FEcase=xc_init.FEcase
# import xc_geom as xcG # Geometry and sets
# import xc_materials as xcM # Materials
import xc_fem_beam as xcFb # FE model
import xc_boundc_beam as xcBb # Boundary conditions
# import xc_loads as xcL # loads
import xc_sets as xcS # sets
import xc_lcases_beam as xcLCb # load cases


# Beam's precamber (selfweight + permanent load + total shrinkage)
# if anything has changed in the model run xc_precamber_calculation.py before
# setting precamber in the beam
import precamber
n_uz=precamber.nod_uz_precamber
for pair in n_uz:
    ntag=pair[0]; deltaZ=pair[1]
    n=xcS.beam.nodes.findTag(ntag)
    pos= n.getInitialPos3d
    pos.z+=deltaZ
    n.setPos(pos)
for e in xcS.beam.elements:
    e.resetNodalCoordinates()
'''
zTopFlange=[n.getCoo[2] for n in xcS.topFlange.nodes]
zMax=max(zTopFlange); zMin=min(zTopFlange); print('precamber (top flange)= ', round((zMax-zMin)*1e3,1),'mm')
zBotFlange=[n.getCoo[2] for n in xcS.bottomFlange.nodes]
zMax=max(zBotFlange); zMin=min(zBotFlange); print('precamber (bottom flange)= ', round((zMax-zMin)*1e3,1),'mm')
'''
# End precamber

analysis=predefined_solutions.simple_static_linear(FEcase)
'''
# Deactivate slab and shear connections
modelSpace.deactivateElements(xcS.shearC, freezeDeadNodes= False)
modelSpace.deactivateElements(xcS.slab,freezeDeadNodes= False)
'''
# Beam self-weight
modelSpace.addLoadCaseToDomain(xcLCb.G1beamSW.name)
result= analysis.analyze(1)
out.displayLoads()
# out.displayDispRot('uX')
# out.displayDispRot('uY')
out.displayDispRot('uZ',defFScale=100)
zBotFlange=[n.getCoo[2] for n in xcS.bottomFlange.nodes]

# Slab self-weight
modelSpace.addLoadCaseToDomain(xcLCb.G2slabSW.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayLoads()
# out.displayDispRot('uX')
# out.displayDispRot('uY')
out.displayDispRot('uZ')


'''
# activate slab and shear connections
modelSpace.activateElements(xcS.shearC)
modelSpace.activateElements(xcS.slab)
'''
# create slab and shear commecions
import xc_fem_slab
import xc_boundc_slab
import xc_lcases_slab as xcLCs


#  shrinkage t=0-15 days
modelSpace.addLoadCaseToDomain(xcLCs.G4shrink_0_15.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')
# out.displayIntForc('M1',xcS.slab)
# out.displayIntForc('M2',xcS.slab)

# Dead load
modelSpace.addLoadCaseToDomain(xcLCs.G3deadL.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')
# out.displayIntForc('M1',xcS.slab)
# out.displayIntForc('M2',xcS.slab)

#  shrinkage t=15-inf days
modelSpace.addLoadCaseToDomain(xcLCs.G4shrink_15_inf.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX',xcS.beam)
out.displayDispRot('uX',xcS.slab)
out.displayDispRot('uY',xcS.beam)
out.displayDispRot('uY',xcS.slab)
out.displayDispRot('uZ',xcS.beam)
out.displayDispRot('uZ',xcS.slab)
#out.displayIntForc('M1',xcS.slab)
#out.displayIntForc('M2',xcS.slab)

# Traffic uniform load
modelSpace.addLoadCaseToDomain(xcLCs.Q1TraffUnif.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')

# Traffic concentrated load
modelSpace.addLoadCaseToDomain(xcLCs.Q2TraffConc.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')


# Heating
modelSpace.addLoadCaseToDomain(xcLCs.Q3heating.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')

# cooling
modelSpace.addLoadCaseToDomain(xcLCs.Q4cooling.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')

# Display Von Mises
modelSpace.calculateNodalReactions(includeInertia=False,reactionCheckTolerance=1e-02)
for e in xcS.beam.elements:
    e.getValuesAtNodes('max_von_mises_stress', False)
out.displayVonMisesStresses(vMisesCode= 'max_von_mises_stress',setToDisplay=xcS.beam)

