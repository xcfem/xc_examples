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
import xc_sets as xcS
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep ; FEcase=xc_init.FEcase
#

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())
grphRltvPath= env.cfg.projectDirTree.getRltvReportSimplLCGrPath()   #relative directory to address the figures in the report
grphPath=env.cfg.projectDirTree.getFullGraphicsPath()+'resSimplLC/' # full path to place the graphics
reportPath=env.cfg.projectDirTree.getFullTextReportPath() # absolute path to place the report
reportFile= reportPath+'report_intForc.tex'  #laTex file where to include the graphics
units=env.cfg.getForceUnitsDescription()
textfl=open(reportFile,'w')  #tex file to be generated

st=xcS.columnZconcrSet
solProc= predefined_solutions.SimpleStaticLinear(FEcase)
solProc.setup()
analysis= solProc.analysis # do not define analysis more than once
for ky in dictLCG.keys():
    lcg=dictLCG[ky]
    lcName=lcg['LCname']
    lcDescr=lcg['description']
    modelSpace.removeAllLoadPatternsFromDomain()
    modelSpace.revertToStart()
    modelSpace.addLoadCaseToDomain(lcName)
    result= analysis.analyze(1)
    fLabel=lcName+st.name+'Mz'
    grFileName=fLabel+'.png'
    caption=lcDescr+'. ' +st.description+'. Momento en eje local Z (kNm)'
    out.displayIntForcDiag(itemToDisp='Mz',setToDisplay=st,fileName= grphPath+grFileName,captionText=caption)
    oh.insertGrInTex(texFile=textfl,grFileNm=grphRltvPath+grFileName,grWdt=env.cfg.grWidth,capText=caption,labl=fLabel)
    fLabel=lcName+st.name+'Vy'
    grFileName=fLabel+'.png'
    caption=lcDescr+'. ' +st.description+'. Esfuerzo cortante en eje local Y (kN)'
    out.displayIntForcDiag(itemToDisp='Vy',setToDisplay=st,fileName= grphPath+grFileName,captionText=caption)
    oh.insertGrInTex(texFile=textfl,grFileNm=grphRltvPath+grFileName,grWdt=env.cfg.grWidth,capText=caption,labl=fLabel)
textfl.write('\\clearpage \n')    
textfl.close()

