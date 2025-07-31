# -*- coding: utf-8 -*-
'''
Lee del fichero «verif_neopren_horizDistort.json» un diccionario con la siguuiente estructura:
{"VE_46":
 {"neopDescr": "Viga 46 p\u00f3rtico Este",
  "neopDim": "150x200x21",
  "deltaMaxParallSlowL": 0.0004717050640366318,
  "deltaMaxParallMixL": 0.0007435900023410838,
  "deltaMaxPerpSlowL": 0.00012572417424556488,
  "deltaMaxPerpMixL": 0.00038071615285950925,
  "combDistortParallSlowL": "G1+Q3A1",
  "distortParallSlowL": 0.022462145906506276,
  "checkDistortParallSlowL": "CUMPLE",
  "combDistortParallMixL": "G1+G2+GNC2+Q1A1+Q1B1+Q1C1+Q1E+Q2A1+Q2B2+Q3A2",
  "distortParallMixL": 0.0354090477305278,
  "checkDistortParallMixL": "CUMPLE",
  "combDistortPerpSlowL": "G1+G2+GNC2+Q3A2",
  "distortPerpSlowL": 0.005986865440264994,
  "checkDistortPerpSlowL": "CUMPLE",
  "combDistortPerpMixL": "G1+G2+GNC2+Q1A10+Q1B1+Q1C10+Q1E+Q2A1+Q2B1+Q3A2",
  "distortPerpMixL": 0.018129340612357582,
  "checkDistortPerpMixL": "CUMPLE"},
 ...
 }
Graba el fichero para la memoria «neopren_horizDistortion_check.tex» con una tabla de resultados de la verificación de distorsión horizontal.

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
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/verif_neopren_horizDistort.json'

if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    neoprResdict= json.load(f)
else:
    print('File '+resultFname+'does not exist')
    quit()
f.close()
texDir=env.cfg.projectDirTree.getFullTextReportPath()
texFileName=texDir+'neopren_horizDistortion_check.tex'

texF=open(texFileName,'w') #
# Distorsión horizontal en dirección paralela al eje de las vigas
head='\\hline & & \\multicolumn{4}{|c|}{\\textsc{Distorsión por acciones lentas}} &  \\multicolumn{4}{|c|}{\\textsc{Distorsión por acciones lentas e instantáneas}} \\\\ \n' + 'Posición apoyo & dimensiones & $\\delta_{max}\ (mm) $ & combinación &  distorsión & verificación & $\\delta_{max}\ (mm) $ & combinación &  distorsión & verificación \\\\ \\hline \n'
caption='Apoyos elastoméricos. Verificación de distorsión horizontal en dirección paralelo al eje de las vigas. \n'
texF.write('\\begin{center} \n \\begin{longtable}{|lc|rlrc|rlrc|} \n  \\caption{'+caption+'} \n   \\\\ \n ' + head + '\\endfirsthead \n '+ head + '\\endhead  \\\\ \hline \n \\multicolumn{10}{r}{\emph{Continúa en la siguiente página}} \\\\ \n \\endfoot \n  \\hline \n \\endlastfoot \n')

for nId in neoprResdict.keys():
    texF.write(neoprResdict[nId]['neopDescr'] +' & '+ neoprResdict[nId]['neopDim'] +  ' & ' + str(round(neoprResdict[nId]['deltaMaxParallSlowL']*1e3,2))+  ' & ' + neoprResdict[nId]['combDistortParallSlowL'] + ' & ' +  str(round(neoprResdict[nId]['distortParallSlowL'],3)) + ' & ' + neoprResdict[nId]['checkDistortParallSlowL'] +  ' & ' + str(round(neoprResdict[nId]['deltaMaxParallMixL']*1e3,2))+  ' & ' + neoprResdict[nId]['combDistortParallMixL'] + ' & ' +  str(round(neoprResdict[nId]['distortParallMixL'],3)) + ' & ' + neoprResdict[nId]['checkDistortParallMixL'] + '\\\\ \n')
texF.write('\\end{longtable} \n')
texF.write('\\end{center}')

# Distorsión horizontal en dirección perpendicular al eje de las vigas
head='\\hline & & \\multicolumn{4}{|c|}{\\textsc{Distorsión por acciones lentas}} &  \\multicolumn{4}{|c|}{\\textsc{Distorsión por acciones lentas e instantáneas}} \\\\ \n' + 'Posición apoyo & dimensiones & $\\delta_{max}\ (mm) $ & combinación &  distorsión & verificación & $\\delta_{max}\ (mm) $ & combinación &  distorsión & verificación  \\\\ \\hline \n'
caption='Apoyos elastoméricos. Verificación de distorsión horizontal en dirección perependicular al eje de las vigas. \n'
texF.write('\\begin{center} \n \\begin{longtable}{|lc|rlrc|rlrc|} \n  \\caption{'+caption+'} \n   \\\\ \n ' + head + '\\endfirsthead \n '+ head + '\\endhead  \\\\ \hline \n \\multicolumn{10}{r}{\emph{Continúa en la siguiente página}} \\\\ \n \\endfoot \n  \\hline \n \\endlastfoot \n')

for nId in neoprResdict.keys():
    texF.write(neoprResdict[nId]['neopDescr'] +' & '+ neoprResdict[nId]['neopDim'] +  ' & ' + str(round(neoprResdict[nId]['deltaMaxPerpSlowL']*1e3,2))+  ' & ' + neoprResdict[nId]['combDistortPerpSlowL'] + ' & ' +  str(round(neoprResdict[nId]['distortPerpSlowL'],3)) + ' & ' + neoprResdict[nId]['checkDistortPerpSlowL'] +  ' & ' + str(round(neoprResdict[nId]['deltaMaxPerpMixL']*1e3,2))+  ' & ' + neoprResdict[nId]['combDistortPerpMixL'] + ' & ' +  str(round(neoprResdict[nId]['distortPerpMixL'],3)) + ' & ' + neoprResdict[nId]['checkDistortPerpMixL'] + '\\\\ \n')
texF.write('\\end{longtable} \n')
texF.write('\\end{center}')

texF.close()
