# -*- coding: utf-8 -*-
import yaml
from pathlib import Path
from postprocess.xcVtk import vtk_graphic_base
from postprocess.config import default_config

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_main_fullmodel

# Common variables
out=xc_init.out
modelSpace=xc_init.modelSpace
prep=xc_init.prep
#
dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())

setsMng=prep.getSets
modelSpace.removeAllLoadPatternsFromDomain()
for ky in dictLCG.keys():
    lcg=dictLCG[ky]
    stName=lcg['setName']; st=setsMng.getSet(stName); lcName=lcg['LCname']
    modelSpace.addLoadCaseToDomain(lcName)
    out.outputStyle.cameraParameters=vtk_graphic_base.CameraParameters(lcg['camera'])
    out.outputStyle.showLoadsPushing=lcg['arrowPush']
    out.displayLoads(setToDisplay=st)
    modelSpace.removeLoadCaseFromDomain(lcName)
