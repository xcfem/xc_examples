# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.reports import report_generator as rprt
from postprocess.config import default_config
# import local modules
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import xc_init
import xc_sets as xcS
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#

# Ordered list of shell-element sets
setsShEl=[xcS.wallSet]
# Ordered list of arguments for shells
# Possible arguments: 'CF', 'N', 'My', 'Mz'
argsShEl= ['CF','N', 'My'] 
# Ordered list of beam-element sets
setsBmEl=[xcS.columnZconcrSet]
# Ordered list of arguments for beams
# Possible arguments: 'CF', 'N', 'My', 'Mz'
argsBmEl=['CF','N','My','Mz']
# Load properties to display:
modelSpace.readControlVars(inputFileName= env.cfg.projectDirTree.getVerifNormStrFile())
limitStateLabel= lsd.normalStressesResistance.label
report=rprt.ReportGenerator(modelSpace,env.cfg)
report.checksReport(limitStateLabel,setsShEl,argsShEl,setsBmEl,argsBmEl)

