'''
Lee del fichero «verif_neopren_vertStress.json» un diccionario con la siguiente estructura:
{"VE_46": {
    "neopDescr": "Viga 46 p\u00f3rtico Este",
    "neopDim": "150x200x21",
    "Nmin": 112884.05112124846,
    "Nmax": 278846.6740739878,
    "combSgmin": "G1+G2+GNC2+Q1A8+Q1B1+Q1C8+Q1E+Q2A1+Q2B2+Q3A2",
    "combSgmax": "G1+G2+Q1A4+Q1B1+Q1E+Q2A2+Q2B1+Q3A2",
    "sgmin": 3762801.704041615,
    "checkSgmin": "CUMPLE",
    "sgmax": 9294889.135799594,
    "checkSgmax": "CUMPLE"},
 ...
 }

Graba el fichero para la memoria «neopren_vertStress_check.tex» con una tabla de resultados de 
las verificaciones de mínimo y máxima tensión vertical en los paratos de apoyo
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
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/verif_neopren_vertStress.json'

if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    neoprResdict= json.load(f)
else:
    print('File '+resultFname+'does not exist')
    quit()
f.close()
texDir=env.cfg.projectDirTree.getFullTextReportPath()
texFileName=texDir+'neopren_vertStress_check.tex'

texF=open(texFileName,'w') #

head='\\hline \n Posición apoyo & dimensiones & $N_{min}\ (kN)$ & combinación &  $\\sigma_{min}\ (MPa)$ & verificación &  $N_{max}\ (kN) $ & combinación & $\\sigma_{max}\ (MPa)$ & verificación  \\\\ \n \\hline \n'
caption='Apoyos elastoméricos. Verificación de tensiones verticales. \n'
texF.write('\\begin{center} \n \\begin{longtable}{|lc|rlrc|rlrc|} \n  \\caption{'+caption+'} \n   \\\\ \n ' + head + '\\endfirsthead \n '+ head + '\\endhead  \\\\ \hline \n \\multicolumn{10}{r}{\emph{Continúa en la siguiente página}} \\\\ \n \\endfoot \n  \\hline \n \\endlastfoot \n')

for nId in neoprResdict.keys():
    texF.write(neoprResdict[nId]['neopDescr'] +' & '+ neoprResdict[nId]['neopDim'] +  ' & ' + str(round(neoprResdict[nId]['Nmin']*1e-3,2))+  ' & ' + neoprResdict[nId]['combSgmin'] + ' & ' +  str(round(neoprResdict[nId]['sgmin']*1e-6,2)) + ' & ' + neoprResdict[nId]['checkSgmin'] +  ' & ' + str(round(neoprResdict[nId]['Nmax']*1e-3,2))+  ' & ' + neoprResdict[nId]['combSgmax'] + ' & ' +  str(round(neoprResdict[nId]['sgmax']*1e-6,2))  +  ' & ' + neoprResdict[nId]['checkSgmax'] + '\\\\ \n')
texF.write('\\end{longtable} \n')
texF.write('\\end{center}')
texF.close()

