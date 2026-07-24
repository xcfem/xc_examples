# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.reports import report_generator as rprt
from postprocess.config import default_config
from materials.strut_and_tie import strut_and_tie_limit_state_checking as lsd
from postprocess.reports import report_generator as rprt
# import local modules
workingDirectory= default_config.setWorkingDirectory()
import env_config
import xc_def_mesh
# Data
cfg=env_config.cfg_P28
setsTrussEl=[xc_def_mesh.diagStrutsSet]
argsTrussEl=['CF','N']
# Common variables
out=xc_def_mesh.out ; modelSpace=xc_def_mesh.modelSpace
#
modelSpace.readControlVars(inputFileName=cfg.projectDirTree.getVerifStrutAndTieFile())
limitStateLabel=lsd.strutAndTieLimitState.label
report=rprt.ReportGenerator(modelSpace,cfg)

report.checksReport(limitStateLabel,setsTrussEl=setsTrussEl,argsTrussEl=argsTrussEl)
