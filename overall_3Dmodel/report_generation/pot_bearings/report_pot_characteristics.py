'''
Read from file pot_data.py the elements and description of POT-bearings and write a report of characteristics
'''
import os
from postprocess.config import default_config
# import local modules
workingDirectory= default_config.setWorkingDirectory()+'/' #search env_config.py
import env_config as env
import pot_report_functions as prf
import pot_data as potD

texDir=env.cfg.projectDirTree.getFullReportPath()
texFileName=texDir+'pot_bearing_caract.tex'
texF=open(texFileName,'w') #

headLongtable=prf.gen_longtable_head(
    headTitles=['Apoyo','$\\Phi$','$F_{vert,med}$','$\\sigma _{vert,med}$', '$\\mu$', '$\\delta_{fric.}$','$K_h$'],
    tit2ndLine=[' ','(mm)','(kN)','(MPa)', ' ', '(mm)','(kN/m)'],
    justif='lrrrrrr',
    caption='Apoyos POT. Dimensiones y características mecánicas',
    
)

texF.write(headLongtable)
for potId in potD.potData.keys():
    potDescr=potD.potData[potId]['potDescr']
    potElem=potD.potData[potId]['potElem']
    potMat=potElem.potMat
    texF.write(potDescr +' & '+ str(int(potMat.d*1e3)) +  ' & ' + str(round(potMat.Fperp*1e-3,2)) +  ' & ' + str(round(potMat.getMeanStress()*1e-6,2)) + ' & ' + str(round(potMat.getMu(),3)) + ' & ' + str(int(potMat.deltaFrict*1e3)) + ' & ' + str(int(potMat.getHorizontalStiffness()*1e-3)) + '\\\\ \n')
texF.write('\\end{longtable} \n')
texF.write('\\end{center}')
texF.close()
