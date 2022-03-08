# -*- coding: utf-8 -*-
import yaml
from pathlib import Path
from postprocess import output_handler



dictLCG=yaml.safe_load(Path('./LC_graph.yaml').read_text())
exec(open("./xc_model.py").read()) #FE model generation

oh= output_handler.OutputHandler(modelSpace)

setsMng=preprocessor.getSets
modelSpace.removeAllLoadPatternsFromDomain()
for ky in dictLCG.keys():
    lcg=dictLCG[ky]
    stName=lcg['setName']; st=setsMng.getSet(stName); lcName=lcg['LCname']
    modelSpace.addLoadCaseToDomain(lcName)
#    oh.outputStyle.cameraParameters=vtk_graphic_base.CameraParameters(lcg['camera'])
#    oh.outputStyle.showLoadsPushing=lcg['arrowPush']
    oh.displayLoads(setToDisplay=st)
    modelSpace.removeLoadCaseFromDomain(lcName)
