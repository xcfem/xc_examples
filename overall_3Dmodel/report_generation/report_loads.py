# -*- coding: utf-8 -*-
import yaml
from pathlib import Path
from postprocess.xcVtk import vtk_graphic_base
from postprocess.config import default_config
from postprocess import output_handler as oh
# import local modules
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import xc_init
import xc_lcases as xcLC
import xc_sets as xcS
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())
setsMng=prep.getSets
pathGrph= env.cfg.projectDirTree.getReportLoadsGrPath()   #directory to place the figures
rltvPath=env.cfg.projectDirTree.getRltvReportLoadsGrPath()
reportFile= env.cfg.projectDirTree.getReportLoadsFile()  #laTex file where to include the graphics
env.cfg.projectDirTree.createTree()
units=env.cfg.getForceUnitsDescription()
textfl=open(reportFile,'w')  #tex file to be generated
modelSpace.removeAllLoadPatternsFromDomain()
for ky in dictLCG.keys():
    lcg=dictLCG[ky]
    stName=lcg['setName']; st=setsMng.getSet(stName); lcName=lcg['LCname']
    modelSpace.addLoadCaseToDomain(lcName)
    capt=lcg['description']
    fLabel=lcName+stName
    grFileName=pathGrph+fLabel+'.png'
    out.displayLoads(setToDisplay=st,fileName= grFileName,caption=capt)
    capt+=', distribución de cargas.'
    rltvGrName=rltvPath+fLabel
    oh.insertGrInTex(texFile=textfl,grFileNm=rltvGrName,grWdt=env.cfg.grWidth,capText=capt,labl=fLabel)
    modelSpace.removeLoadCaseFromDomain(lcName)
textfl.close()
