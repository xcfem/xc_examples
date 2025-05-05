# Calculate the beam precamber (selfweight + permanent load + total shrinkage)
# saves the pairs [node_tag,uz] in list nod_uz_precamber written to the file
# precamber.py
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

analysis=predefined_solutions.simple_static_linear(FEcase)
# Beam self-weight
modelSpace.addLoadCaseToDomain(xcLCb.G1beamSW.name)
result= analysis.analyze(1)
# Slab self-weight
modelSpace.addLoadCaseToDomain(xcLCb.G2slabSW.name)
result= analysis.analyze(1)
# create slab and shear commecions
import xc_fem_slab
import xc_boundc_slab
import xc_lcases_slab as xcLCs
#  shrinkage t=0-15 days
modelSpace.addLoadCaseToDomain(xcLCs.G4shrink_0_15.name)
result= analysis.analyze(1)
# Dead load
modelSpace.addLoadCaseToDomain(xcLCs.G3deadL.name)
result= analysis.analyze(1)
#  shrinkage t=15-inf days
modelSpace.addLoadCaseToDomain(xcLCs.G4shrink_15_inf.name)
result= analysis.analyze(1)

nod_uz_precamber=list()
for n in xcS.beam.nodes:
    uz=n.getDispXYZ[2]
    nod_uz_precamber.append([n.tag,-uz])

f=open('./precamber.py','w')

