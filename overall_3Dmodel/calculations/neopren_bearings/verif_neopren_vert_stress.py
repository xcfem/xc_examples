# -*- coding: utf-8 -*-
''' Lee del fichero 'neopren_bearing_results.json' el diccionario neoprDatasdict con los resultados de esfuerzos y deformaciones obtenidos en cada caso de carga. Este diccionario tiene la siguiente estructura:
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
Con estos datos realiza las verificaciones de mínimo y máxima tensión vertical 
y escribe los resultados de esta verificación en el fichero 
«verif_neopren_vertStress.json» con la siguiente estructura:

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
'''


import combNeopren 

# Data
sigma_min_adm= 3e6 # allowable minimum stress over neopren (Pa)
sigma_max_adm= 12e6 # allowable maximum stress over neopren (Pa)
combs2check=combNeopren.mixComb

# End data

import os
import json
from solution import predefined_solutions
from postprocess.config import default_config
import yaml
from pathlib import Path

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
# Json file with dictionary of results (resDict)

inputFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/neopren_bearing_results.json'

outputFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/verif_neopren_vertStress.json'

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())

if os.path.isfile(inputFname):
    f=open(inputFname,'r') # Open JSON file
    neoprDatasdict= json.load(f)
else:
    print("Can't find file:',inputFname")
    quit()

f.close()

# Dictionary with verification of neoprene vertical stress 
neoprVertStressDict=dict()
for n in  neoprDatasdict.keys():
    dataDict=neoprDatasdict[n]
    neoprVertStressDict[n]=dict()
    neoprVertStressDict[n]['neopDescr']=dataDict['neopDescr']
    neoprVertStressDict[n]['neopDim']=dataDict['neopDim']
    dataRDict=neoprDatasdict[n]['LCres']
    neoprVertStressDict[n]['Nmin']=1e20
    neoprVertStressDict[n]['Nmax']=0
    dimLst=dataDict['neopDim'].split('x')
    dimPar,dimPerp,eneto=[int(d)*1e-3 for d in dimLst] # dimensiones de neopreno: paralelo a la viga, perpendicular a la viga, espesor neto
    for cmb in combs2check:
        lstLC=cmb.replace(' ','').split('+')
        N=sum([-dataRDict[lc]['Rz'] for lc in lstLC])
        if N < neoprVertStressDict[n]['Nmin']:
            neoprVertStressDict[n]['Nmin']=N
            neoprVertStressDict[n]['combSgmin']=cmb
        if N > neoprVertStressDict[n]['Nmax']:
            neoprVertStressDict[n]['Nmax']=N
            neoprVertStressDict[n]['combSgmax']=cmb
    neoprVertStressDict[n]['sgmin']=neoprVertStressDict[n]['Nmin']/(dimPar*dimPerp)
    neoprVertStressDict[n]['checkSgmin'] = 'CUMPLE' if neoprVertStressDict[n]['sgmin'] > sigma_min_adm else 'ANCLADO'
    neoprVertStressDict[n]['sgmax']=neoprVertStressDict[n]['Nmax']/(dimPar*dimPerp)
    neoprVertStressDict[n]['checkSgmax'] = 'CUMPLE' if neoprVertStressDict[n]['sgmax'] < sigma_max_adm else  'NO CUMPLE'

# Dump results
with open(outputFname,'w') as f:
    json.dump(neoprVertStressDict,f)
f.close()

