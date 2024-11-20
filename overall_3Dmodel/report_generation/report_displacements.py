# -*- coding: utf-8 -*-
from solution import predefined_solutions
from postprocess.config import default_config
import yaml
from pathlib import Path
from postprocess import output_handler as oh
# import local modules
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import xc_init
import xc_main_fullmodel
import xc_lcases as xcLC
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep ; FEcase=xc_init.FEcase
#

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())
grphRltvPath= env.cfg.projectDirTree.getRltvReportSimplLCGrPath()   #relative directory to address the figures in the report
grphPath=env.cfg.projectDirTree.getFullGraphicsPath()+'resSimplLC/' # full path to place the graphics
reportPath=env.cfg.projectDirTree.getFullTextReportPath() # absolute path to place the report
reportFile= reportPath+'report_displacements.tex'  #laTex file where to include the graphics

textfl=open(reportFile,'w')  #tex file to be generated
for ky in dictLCG.keys():
    lcg=dictLCG[ky]
    lcName=lcg['LCname']
    lcDescr=lcg['description']
    modelSpace.removeAllLoadPatternsFromDomain()
    modelSpace.revertToStart()
    modelSpace.addLoadCaseToDomain(lcName)
    analysis= predefined_solutions.simple_static_linear(FEcase)
    result= analysis.analyze(1)
    fLabel=lcName+'uX'
    grFileName=fLabel+'.png'
    caption=lcDescr+'. Desplazamiento transversal X (mm)'
    out.displayDispRot(itemToDisp='uX',setToDisplay=None,fileName= grphPath+grFileName,captionText=caption)
    oh.insertGrInTex(texFile=textfl,grFileNm=grphRltvPath+grFileName,grWdt=env.cfg.grWidth,capText=caption,labl=fLabel)
    fLabel=lcName+'uY'
    grFileName=fLabel+'.png'
    caption=lcDescr+'. Desplazamiento longitudinal Y (mm)'
    out.displayDispRot(itemToDisp='uY',setToDisplay=None,fileName= grphPath+grFileName,captionText=caption)
    oh.insertGrInTex(texFile=textfl,grFileNm=grphRltvPath+grFileName,grWdt=env.cfg.grWidth,capText=caption,labl=fLabel)
    fLabel=lcName+'uZ'
    grFileName=fLabel+'.png'
    caption=lcDescr+'. Desplazamiento vertical Z (mm)'
    out.displayDispRot(itemToDisp='uZ',setToDisplay=None,fileName= grphPath+grFileName,captionText=caption)
    oh.insertGrInTex(texFile=textfl,grFileNm=grphRltvPath+grFileName,grWdt=env.cfg.grWidth,capText=caption,labl=fLabel)
    
textfl.write('\\clearpage \n')    
textfl.close()

