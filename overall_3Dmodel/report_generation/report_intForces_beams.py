# -*- coding: utf-8 -*-
from solution import predefined_solutions
from postprocess.config import default_config
import yaml
from pathlib import Path
from postprocess import output_handler as oh

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import xc_model as model #FE model generation
import load_case_definition as LCdef

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())

grphRltvPath= env.cfg.projectDirTree.getRltvReportSimplLCGrPath()   #relative directory to address the figures in the report
grphPath=env.cfg.projectDirTree.getFullGraphicsPath()+'resSimplLC/' # full path to place the graphics
reportPath=env.cfg.projectDirTree.getFullTextReportPath() # absolute path to place the report
reportFile= reportPath+'report_intForc_beams.tex'  #laTex file where to include the graphics
units=env.cfg.getForceUnitsDescription()

#LCGs2display=LCdef.LCG_perm
#LCGs2display=LCdef.LCG_vert
#LCGs2display=LCdef.LCG_fren
#LCGs2display=LCdef.LCG_centr
#LCGs2display=LCdef.LCG_lazo+LCdef.LCG_paseos+LCdef.LCG_viento
LCGs2display=LCdef.LCG_term+LCdef.LCG_acc
textfl=open(reportFile,'a')  #tex file to be generated
st=model.beams
for ky in LCGs2display:
    lcg=dictLCG[ky]
    lcName=lcg['LCname']
    lcDescr=lcg['description']
    model.modelSpace.removeAllLoadPatternsFromDomain()
    model.modelSpace.revertToStart()
    model.modelSpace.addLoadCaseToDomain(lcName)
    analysis= predefined_solutions.simple_static_linear(model.FEcase)
    result= analysis.analyze(1)
    fLabel=lcName+'beamsMz'
    grFileName=fLabel+'.png'
    caption=lcDescr+'. Vigas, momento en eje fuerte (kNm)'
    model.out.displayIntForcDiag(itemToDisp='Mz',setToDisplay=st,fileName= grphPath+grFileName,captionText=caption)
    oh.insertGrInTex(texFile=textfl,grFileNm=grphRltvPath+grFileName,grWdt=env.cfg.grWidth,capText=caption,labl=fLabel)
    fLabel=lcName+'beamsVy'
    grFileName=fLabel+'.png'
    caption=lcDescr+'. Vigas, esfuerzo cortante vertical (kN)'
    model.out.displayIntForcDiag(itemToDisp='Vy',setToDisplay=st,fileName= grphPath+grFileName,captionText=caption)
    oh.insertGrInTex(texFile=textfl,grFileNm=grphRltvPath+grFileName,grWdt=env.cfg.grWidth,capText=caption,labl=fLabel)
    
textfl.write('\\clearpage \n')    
textfl.close()

