'''
Lee del fichero 'pot_bearing_results.json' el diccionario neoprResdict con los resultados de esfuerzos y deformaciones obtenidos en cada caso de carga. La estructura del diccionario es la siguiente:
{"PU-P1":
 {"potDescr": "PU pila 1",
  "potDiam": 0.400,
  "deltaFric": 0.02,
  "Kh": 2400000.0
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
            ...}
  ..}
 }

Graba el fichero para la memoria «pot_bearing_results.tex» con una tabla de esfuerzos y deformaciones en los aparatos de apoyo
'''
import json
import os
from postprocess.config import default_config
import yaml
# import local modules
workingDirectory= default_config.setWorkingDirectory()+'/' #search env_config.py
import env_config as env
import pot_report_functions as prf

# create or read json file
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'potBearing/pot_bearing_results.json'
if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    potResdict= json.load(f)
else:
    print('File '+resultFname+'does not exist')
    quit()
f.close()

texDir=env.cfg.projectDirTree.getFullReportPath()
texFileName=texDir+'pot_bearing_results.tex'

texF=open(texFileName,'w') #
LCs2tex=list()
potId=next(iter(potResdict))
for lc in potResdict[potId]['LCres'].keys():
    LCs2tex.append([lc,potResdict[potId]['LCres'][lc]['loadDescr']])


headLongtable=prf.gen_longtable_head(
    headTitles=['Apoyo','$F_{long.}$','$F_{trv.}$','$F_{vert.}$','$u_{long.}$','$u_{trv.}$','$\\alpha_{long.}$','$\\alpha_{trv.}$'],
    tit2ndLine=[' ','(kN)','(kN)','(kN)','(mm)','(mm)','$\\times 10^{-2}$ rad', '$\\times 10^{-2} rad$'],
    justif='lrrrrrrr',
    caption='Apoyos POT. Esfuerzos, desplazamientos y giros por hipótesis',
    )
texF.write(headLongtable)
for lc in LCs2tex:
    lcName=lc[0]
    lcDescr=lc[1]
    hipText='Hipótesis '+ lcDescr
    texF.write('\\hline \n \\multicolumn{8}{c}{'+hipText+'} \\\\ \n \\hline \n') 
    for potId in potResdict.keys():
        texF.write(potResdict[potId]['potDescr'] +' & ' + str(round(potResdict[potId]['LCres'][lcName]['Rx']*1e-3,2)) + ' & ' + str(round(potResdict[potId]['LCres'][lcName]['Ry']*1e-3,2)) + ' & ' + str(round(potResdict[potId]['LCres'][lcName]['Rz']*1e-3,2)) + ' & ' + str(round(potResdict[potId]['LCres'][lcName]['dispX']*1e3,1)) + ' & ' + str(round(potResdict[potId]['LCres'][lcName]['dispY']*1e3,2)) +  ' & ' + str(round(potResdict[potId]['LCres'][lcName]['rotX']*1e2,3))  + ' & ' + str(round(potResdict[potId]['LCres'][lcName]['rotY']*1e2,3))  + '\\\\ \n')
        
texF.write('\\end{longtable} \n')
texF.write('\\end{center}')
texF.close()
