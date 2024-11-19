# -*- coding: utf-8 -*-
from postprocess.config import default_config

# import local modules
workingDirectory= default_config.setWorkingDirectory() 
import xc_init
import xc_sets as xcS
out=xc_init.out

setsTodisp=[xcS.decklv1Set,xcS.decklv2Set,xcS.footSet,xcS.wallSet,xcS.columnZconcrSet,xcS.columnZsteelSet,xcS.beamYSet,xcS.beamXconcrSet,xcS.beamXsteelSet]

out.displayFEMesh(setsToDisplay=setsTodisp,caption=None,fileName=None,defFScale=0.0)

