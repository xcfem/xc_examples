# -*- coding: utf-8 -*-
from solution import predefined_solutions
from postprocess.config import default_config

# import local modules
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import xc_init
import xc_main_fullmodel
import xc_lcases as xcLC
import xc_sets as xcS

# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep ; FEcase=xc_init.FEcase
#
analysis= predefined_solutions.simple_static_linear(FEcase)
for ls in [xcLC.QearthPressWall]:#,xcLC.QearthPWallStrL]:
    modelSpace.removeAllLoadPatternsFromDomain()
    modelSpace.addLoadCaseToDomain(ls.name)
    result= analysis.analyze(1)
    out.displayDispRot('uX')
    out.displayDispRot('uY')
    out.displayDispRot('uZ')
    out.displayIntForc('N1',xcS.wallSet)
    out.displayIntForc('N2',xcS.wallSet)
    out.displayIntForc('N12',xcS.wallSet)
    out.displayIntForc('Q1',xcS.wallSet)
    out.displayIntForc('Q2',xcS.wallSet)
    out.displayIntForc('M1',xcS.wallSet)
    out.displayIntForc('M2',xcS.wallSet)
    out.displayIntForc('M12',xcS.wallSet)
    
