#from scipy.constants import g
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_boundc_beam as xcBb
import xc_lcases as xcLC

prep=xc_init.prep ; modelSpace=xc_init.modelSpace; out=xc_init.out; FEcase=xc_init.FEcase
total=prep.getSets.getSet('total')

from solution import predefined_solutions
solProc= predefined_solutions.SimpleStaticLinear(FEcase)
solProc.setup()
analysis= solProc.analysis
for lcNm in (xcLC.lstLCnames):
    modelSpace.removeAllLoadPatternsFromDomain()
    modelSpace.revertToStart()
    modelSpace.addLoadCaseToDomain(lcNm)
    result= analysis.analyze(1)
    modelSpace.calculateNodalReactions(True)
    totalRx=0
    totalRy=0
    totalRz=0
    for n in total.nodes:
        totalRx+=n.getReactionForce3d[0]
        totalRy+=n.getReactionForce3d[1]
        totalRz+=n.getReactionForce3d[2]
    print(lcNm,' Rx=', round(totalRx*1e-3,0),' Ry=', round(totalRy*1e-3,0),' kN,  Rz=', round(totalRz*1e-3,0),' kN')
