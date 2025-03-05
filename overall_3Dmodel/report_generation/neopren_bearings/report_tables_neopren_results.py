'''
Lee del fichero 'neopren_bearing_results.json' el diccionario neoprResdict con los resultados de esfuerzos y deformaciones obtenidos en cada caso de carga. La estructura del diccionario es la siguiente:
{"VE_46":
 {"neopDescr": "Viga 46 p\u00f3rtico Este",
  "neopDim": "150x200x21",
  "LCres": {"G1":
            {"loadDescr": " G1: peso propio",
             "Rx": -250.72122578898671,
             "Ry": -51.79004697611652,
             "Rz": -165175.49368822575,
             "Mx": 1.070603892666845,
             "My": 22.452446033500646,
             "Mz": -0.333896693765817,
             "dispX": -0.0002193810725653634,
             "dispY": -4.531629110410196e-05,
             "dispZ": -0.0001927047426362634,
             "rotX": 6.604468179470516e-05,
             "rotY": 0.00043824578593320635,
             "rotZ": -4.072856975535637e-05},
            ...}
  ..}
 }
Graba el fichero para la memoria «neopren_bearing_results.tex» con una tabla de esfuerzos y deformaciones en los aparatos de apoyo
'''
import json
import os
from postprocess.config import default_config
from misc_utils import data_struct_utils as dsu
from postprocess import output_handler as oh
from postprocess.config import default_config
import yaml
# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env


# read json file
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/neopren_bearing_results.json'
if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    neoprResdict= json.load(f)
else:
    print('File '+resultFname+'does not exist')
    quit()
f.close()

texDir=env.cfg.projectDirTree.getFullTextReportPath()
texFileName=texDir+'neopren_bearing_results.tex'

texF=open(texFileName,'w') #
LCs2tex=list()
nId=next(iter(neoprResdict))
for lc in neoprResdict[nId]['LCres'].keys():
    LCs2tex.append([lc,neoprResdict[nId]['LCres'][lc]['loadDescr']])

head='\\hline \n Posición apoyo & dimensiones & $F_x\ (kN)$ & $F_y\ (kN)$ & $F_z\ (kN)$ & $M_x\ (kNm)$ & $M_y\ (kNm)$ & $M_z\ (kNm)$ & $u_x\ (mm)$ &$u_y\ (mm)$ & $u_z\ (mm)$ & $\\theta_x\ (rad$ &$\\theta_y\ (rad)$ & $\\theta_z\ (rad)$ \\\\ \n \\hline \n'
for lc in LCs2tex:
    lcName=lc[0]
    lcDescr=lc[1]
    caption='Apoyos elastoméricos. Esfuerzos, desplazamientos y giros en hipótesis '+ lcDescr+ '. \n'
    texF.write('\\begin{center} \n \\begin{longtable}{|lcrrrrrrrrrrrr|} \n  \\caption{'+caption+'} \n   \\\\ \n ' + head + '\\endfirsthead \n '+ head + '\\endhead  \\\\ \hline \n \\multicolumn{14}{r}{\emph{Continúa en la siguiente página}} \\\\ \n \\endfoot \n  \\hline \n \\endlastfoot \n')
    for nId in neoprResdict.keys():
        texF.write(neoprResdict[nId]['neopDescr'] +' & '+ neoprResdict[nId]['neopDim'] +  ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['Rx']*1e-3,2)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['Ry']*1e-3,2)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['Rz']*1e-3,2)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['Mx']*1e-3,2)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['My']*1e-3,2)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['Mz']*1e-3,2)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['dispX']*1e3,1)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['dispY']*1e3,2)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['dispZ']*1e3,2)) + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['rotX'],5))  + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['rotY'],5))  + ' & ' + str(round(neoprResdict[nId]['LCres'][lcName]['rotZ'],5)) + '\\\\ \n')
    texF.write('\\end{longtable} \n')
    texF.write('\\end{center}')
texF.close()
