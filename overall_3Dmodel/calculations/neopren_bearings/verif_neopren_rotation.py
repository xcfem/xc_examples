# -*- coding: utf-8 -*-
''' Lee del fichero «neopren_bearing_results.json» el diccionario neoprDatasdict con los resultados de esfuerzos y deformaciones obtenidos en cada caso de carga . Este diccionario tiene la siguiente estructura:
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

Con estos datos, realiza la verificaciones de rotación máxima y graba el resultado en el fichero «verif_neopren_rotation.json», con la siguiente estructura:
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
'''

import combNeopren 

# Data
t_layer_elastom=7e-3 # espesor de cada capa de elastómero (bocadillo básico)
n_layers=3 # número de capas
rot0=0.003 #0.01 # giro inicial por falta de paralelismo entre tablero y apoyos (0.003 en tableros hormigonados in situ y metálicos, 0.01 en tableros pregabricados.
G=800e3  #módulo de cortante del material elastomérico
rotAxis2check='Y' # eje en torno al cual se produce la rotación del neopreno 
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

outputFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/verif_neopren_rotation.json'

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())

if os.path.isfile(inputFname):
    f=open(inputFname,'r') # Open JSON file
    neoprDatasdict= json.load(f)
else:
    print("Can't find file:',inputFname")
    quit()

f.close()

# Dictionary with verification of neoprene vertical stress 
neoprRotationDict=dict()
for n in  neoprDatasdict.keys():
    dataDict=neoprDatasdict[n]
    neoprRotationDict[n]=dict()
    neoprRotationDict[n]['neopDescr']=dataDict['neopDescr']
    neoprRotationDict[n]['neopDim']=dataDict['neopDim']
    dataRDict=neoprDatasdict[n]['LCres']
    neoprRotationDict[n]['rotMax']=0
    dimLst=dataDict['neopDim'].split('x')
    dimPar,dimPerp,eneto=[int(d)*1e-3 for d in dimLst] # dimensiones de neopreno: paralelo a la viga, perpendicular a la viga, espesor neto
    S=dimPar*dimPerp/(2*t_layer_elastom*(dimPar+dimPerp)) # factor de forma
    sigma=0
    for cmb in combs2check:
        lstLC=cmb.replace(' ','').split('+')
        rot=abs(sum([dataRDict[lc]['rot'+rotAxis2check] for lc in lstLC]))
        if rot > neoprRotationDict[n]['rotMax']:
            neoprRotationDict[n]['rotMax']=rot
            N=sum([-dataRDict[lc]['Rz'] for lc in lstLC])
            sigma=N/(dimPar*dimPerp)
            neoprRotationDict[n]['combRotMax']=cmb
    neoprRotationDict[n]['rotTotal']=neoprRotationDict[n]['rotMax']+rot0 # rotación a abrorber con el neopreno
    neoprRotationDict[n]['rotAdmsbl']=n_layers*3/S*(t_layer_elastom/dimPar)**2*sigma/G
    neoprRotationDict[n]['checkRotation'] = 'CUMPLE' if neoprRotationDict[n]['rotTotal'] < neoprRotationDict[n]['rotAdmsbl'] else 'NO CUMPLE'

# Dump results
with open(outputFname,'w') as f:
    json.dump(neoprRotationDict,f)
f.close()

