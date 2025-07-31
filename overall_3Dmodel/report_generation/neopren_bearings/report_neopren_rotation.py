# -*- coding: utf-8 -*-
'''
Lee del fichero «verif_neopren_rotation.json» un diccionario con la siguiente estructura:
{"VE_46":
 {"neopDescr": "Viga 46 p\u00f3rtico Este",
  "neopDim": "150x200x21",
  "rotMax": 0.0005299531569969836,
  "combRotMax": "G1+G2+Q1A10+Q1B1+Q1E+Q2A2+Q2B1+Q3A2",
  "rotTotal": 0.0035299531569969837,
  "rotAdmsbl": 0.03683000110349873,
  "checkRotation": "CUMPLE"},
 ...
 }
Graba el fichero para la memoria «neopren_rotation_check.tex» con una tabla de resultados de la verificación de rotación. 
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
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/verif_neopren_rotation.json'

if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    neoprResdict= json.load(f)
else:
    print('File '+resultFname+'does not exist')
    quit()
f.close()
texDir=env.cfg.projectDirTree.getFullTextReportPath()
texFileName=texDir+'neopren_rotation_check.tex'

texF=open(texFileName,'w') #

head='\\hline \n Posición apoyo & dimensiones & $\\theta_{max,calc}\ (rad)$ & combinación &  $\\theta_{max,calc}+\\theta_0\ (rad)$ &  $\\theta_{admisible}\ (rad)$ & verificación  \\\\ \n \\hline \n'
caption='Apoyos elastoméricos. Verificación de giro admisible. \n'
texF.write('\\begin{center} \n \\begin{longtable}{|lc|rlrrc|} \n  \\caption{'+caption+'} \n   \\\\ \n ' + head + '\\endfirsthead \n '+ head + '\\endhead  \\\\ \hline \n \\multicolumn{7}{r}{\emph{Continúa en la siguiente página}} \\\\ \n \\endfoot \n  \\hline \n \\endlastfoot \n')

for nId in neoprResdict.keys():
    texF.write(neoprResdict[nId]['neopDescr'] +' & '+ neoprResdict[nId]['neopDim'] +  ' & ' + str(round(neoprResdict[nId]['rotMax'],4))+  ' & ' + neoprResdict[nId]['combRotMax'] +  ' & ' +  str(round(neoprResdict[nId]['rotTotal'],4)) + ' & ' +  str(round(neoprResdict[nId]['rotAdmsbl'],4)) + ' & ' + neoprResdict[nId]['checkRotation'] + '\\\\ \n')
texF.write('\\end{longtable} \n')
texF.write('\\end{center}')
texF.close()


