# -*- coding: utf-8 -*-
from solution import predefined_solutions
from postprocess.config import default_config

# import local modules
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import xc_init
import xc_boundc_beam
import xc_fem
import xc_fem_slab
#import xc_main_fullmodel
import xc_lcases as xcLC
import xc_sets as xcS

# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep ; FEcase=xc_init.FEcase
#
analysis= predefined_solutions.simple_static_linear(FEcase)
import xc_fem_slab
for lcNm in xcLC.lstLCnmPostSlab:
    modelSpace.removeAllLoadPatternsFromDomain()
    modelSpace.addLoadCaseToDomain(lcNm)
    result= analysis.analyze(1)
    out.displayDispRot('uZ')
