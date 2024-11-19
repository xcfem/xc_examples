# -*- coding: utf-8 -*-
import yaml
from pathlib import Path
from postprocess.xcVtk import vtk_graphic_base
from postprocess.config import default_config
from postprocess import output_handler as oh

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import xc_model as model #FE model generation
import load_case_definition as LCdef

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())

setsMng=model.prep.getSets
pathGrph= env.cfg.projectDirTree.getReportLoadsGrPath()   #directory to place the figures
rltvPath=env.cfg.projectDirTree.getRltvReportLoadsGrPath()
reportFile= env.cfg.projectDirTree.getReportLoadsFile()  #laTex file where to include the graphics
env.cfg.projectDirTree.createTree()
units=env.cfg.getForceUnitsDescription()

textfl=open(reportFile,'w')  #tex file to be generated

model.modelSpace.removeAllLoadPatternsFromDomain()
for ky in dictLCG.keys():
    lcg=dictLCG[ky]
    stName=lcg['setName']; st=setsMng.getSet(stName); lcName=lcg['LCname']
    model.modelSpace.addLoadCaseToDomain(lcName)
    capt=lcg['description']
    fLabel=lcName+stName
    grFileName=pathGrph+fLabel+'.png'
    model.out.displayLoads(setToDisplay=st,fileName= grFileName,caption=capt)
    capt+=', distribución de cargas.'
    rltvGrName=rltvPath+fLabel
    oh.insertGrInTex(texFile=textfl,grFileNm=rltvGrName,grWdt=env.cfg.grWidth,capText=capt,labl=fLabel)
    model.modelSpace.removeLoadCaseFromDomain(lcName)
textfl.close()
