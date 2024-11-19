# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.reports import report_generator as rprt
from postprocess.config import default_config

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import xc_model as model #FE model generation
import load_case_definition as lCases


#ordered list of load cases (from those defined in ../load_state_data.py
#or redefined lately) to be displayed:
loadCasesToDisplay=[lCases.G1]

textfl=open(env.cfg.reportSimplLCFile,'w')  #tex file to be generated
for lc in loadCasesToDisplay:
    lc.simplLCReports(FEproblem=FEcase,pathGr= env.cfg.reportSimplLCGrPath,texFile=textfl,grWdt= cfg.grWidth,capStdTexts= cfg.capTexts)

textfl.close()

