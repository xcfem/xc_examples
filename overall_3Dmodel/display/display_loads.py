# -*- coding: utf-8 -*-
import yaml
from pathlib import Path
from postprocess.xcVtk import vtk_graphic_base
from postprocess.config import default_config

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import model_gen as model #FE model generation

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())

setsMng=model.prep.getSets
model.modelSpace.removeAllLoadPatternsFromDomain()
for ky in dictLCG.keys():
    lcg=dictLCG[ky]
    stName=lcg['setName']; st=setsMng.getSet(stName); lcName=lcg['LCname']
    model.modelSpace.addLoadCaseToDomain(lcName)
    model.out.outputStyle.cameraParameters=vtk_graphic_base.CameraParameters(lcg['camera'])
    model.out.outputStyle.showLoadsPushing=lcg['arrowPush']
    model.out.displayLoads(setToDisplay=st)
    model.modelSpace.removeLoadCaseFromDomain(lcName)
