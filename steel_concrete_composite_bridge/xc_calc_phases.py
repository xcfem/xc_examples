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
import xc_lcases as xcLC # load cases

analysis=predefined_solutions.simple_static_linear(FEcase)
'''
# Deactivate slab and shear connections
modelSpace.deactivateElements(xcS.shearC, freezeDeadNodes= False)
modelSpace.deactivateElements(xcS.slab,freezeDeadNodes= False)
'''
# Beam self-weight
modelSpace.addLoadCaseToDomain(xcLC.G1beamSW.name)
result= analysis.analyze(1)
out.displayLoads()
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')

# Slab self-weight
modelSpace.addLoadCaseToDomain(xcLC.G2slabSW.name)
#out.displayLoads()
result= analysis.analyze(1)
out.displayLoads()
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')
out.displayIntForc('M1',xcS.slab)
out.displayIntForc('M2',xcS.slab)

'''
# activate slab and shear connections
modelSpace.activateElements(xcS.shearC)
modelSpace.activateElements(xcS.slab)
'''
# create slab and shear commecions
import xc_fem_slab
out.displayIntForc('M1',xcS.slab)
out.displayIntForc('M2',xcS.slab)

# Dead load

modelSpace.addLoadCaseToDomain(xcLC.G3deadL.name)
out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')

out.displayDispRot('uY')
out.displayDispRot('uZ')
out.displayIntForc('M1',xcS.slab)
out.displayIntForc('M2',xcS.slab)

# Traffic uniform load
modelSpace.addLoadCaseToDomain(xcLC.Q1TraffUnif.name)
out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')
out.displayIntForc('M1',xcS.slab)
out.displayIntForc('M2',xcS.slab)

# Traffic concentrated load
modelSpace.addLoadCaseToDomain(xcLC.Q2TraffConc.name)
out.displayLoads()
result= analysis.analyze(1)
out.displayDispRot('uX')
out.displayDispRot('uY')
out.displayDispRot('uZ')
out.displayIntForc('M1',xcS.slab)
out.displayIntForc('M2',xcS.slab)
