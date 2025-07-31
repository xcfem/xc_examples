# -*- coding: utf-8 -*-
''' Lee del fichero «neopren_bearing_results.json» el diccionario neoprDatasdict con los resultados de esfuerzos y deformaciones obtenidos en cada caso de carga. Este diccionario tiene la siguiente estructura:
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

Con estos datos realiza las verificaciones de distorsión hrizontal y graba los resultados de estas verificaciones en el fichero  «verif_neopren_horizDistort.json», organizados en un diccionario con esta estructura:

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
'''

import combNeopren 
# Data
slowL_distort_adm= 0.5 # allowable maximum horizontal distortion for slow loads.
mixL_distort_adm= 0.7 # allowable maximum horizontal distortion for mixed loads.
slowLcombs2check=['G1+GNC2',
                  'G1+GNC2+Q3A1',
                  'G1+GNC2+Q3A2',
                  'G1+Q3A1',
                  'G1+Q3A1',
                  'G1+G2+GNC2',
                  'G1+G2+GNC2+Q3A1',
                  'G1+G2+GNC2+Q3A2',
                  'G1+G2+Q3A1',
                  'G1+G2+Q3A1',
                   ]
mixLcombs2check=combNeopren.mixComb
dirParall='X' # dirección paralela a la viga o dintel (dimensiones del neopreno expresadas como dimParallxdimPerpxespesorNeto
dirPerp='Y' # dirección perpendicular a la viga o dintel 
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

outputFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/verif_neopren_horizDistort.json'

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())

if os.path.isfile(inputFname):
    f=open(inputFname,'r') # Open JSON file
    neoprDatasdict= json.load(f)
else:
    print("Can't find file:',inputFname")
    quit()
f.close()

# Dictionary with verification of neoprene vertical stress 
neoprHorizDistortDict=dict()
for n in  neoprDatasdict.keys():
    dataDict=neoprDatasdict[n]
    neoprHorizDistortDict[n]=dict()
    neoprHorizDistortDict[n]['neopDescr']=dataDict['neopDescr']
    neoprHorizDistortDict[n]['neopDim']=dataDict['neopDim']
    dataRDict=neoprDatasdict[n]['LCres']
    neoprHorizDistortDict[n]['deltaMaxParallSlowL']=0
    neoprHorizDistortDict[n]['deltaMaxParallMixL']=0
    neoprHorizDistortDict[n]['deltaMaxPerpSlowL']=0
    neoprHorizDistortDict[n]['deltaMaxPerpMixL']=0
    dimLst=dataDict['neopDim'].split('x')
    dimPar,dimPerp,eneto=[int(d)*1e-3 for d in dimLst] # dimensiones de neopreno: paralelo a la viga, perpendicular a la viga, espesor neto
    for cmb in slowLcombs2check:
        lstLC=cmb.replace(' ','').split('+')
        # Distorsión en dirección paralela a la viga o dintel
        delta=abs(sum([dataRDict[lc]['disp'+dirParall] for lc in lstLC]))
        if delta > neoprHorizDistortDict[n]['deltaMaxParallSlowL']:
            neoprHorizDistortDict[n]['deltaMaxParallSlowL']=delta
            neoprHorizDistortDict[n]['combDistortParallSlowL']=cmb
    neoprHorizDistortDict[n]['distortParallSlowL']=neoprHorizDistortDict[n]['deltaMaxParallSlowL']/eneto
    neoprHorizDistortDict[n]['checkDistortParallSlowL'] = 'CUMPLE' if neoprHorizDistortDict[n]['distortParallSlowL'] < slowL_distort_adm else 'NO CUMPLE'
    for cmb in mixLcombs2check:
        lstLC=cmb.replace(' ','').split('+')
        delta=abs(sum([dataRDict[lc]['disp'+dirParall] for lc in lstLC]))
        if delta > neoprHorizDistortDict[n]['deltaMaxParallMixL']:
            neoprHorizDistortDict[n]['deltaMaxParallMixL']=delta
            neoprHorizDistortDict[n]['combDistortParallMixL']=cmb
    neoprHorizDistortDict[n]['distortParallMixL']=neoprHorizDistortDict[n]['deltaMaxParallMixL']/eneto
    neoprHorizDistortDict[n]['checkDistortParallMixL']='CUMPLE' if neoprHorizDistortDict[n]['distortParallMixL'] < mixL_distort_adm else 'NO CUMPLE'
    for cmb in slowLcombs2check:
        lstLC=cmb.replace(' ','').split('+')
        # Distorsión en dirección perpendicular a la viga o dintel
        delta=abs(sum([dataRDict[lc]['disp'+dirPerp] for lc in lstLC]))
        if delta > neoprHorizDistortDict[n]['deltaMaxPerpSlowL']:
            neoprHorizDistortDict[n]['deltaMaxPerpSlowL']=delta
            neoprHorizDistortDict[n]['combDistortPerpSlowL']=cmb
    neoprHorizDistortDict[n]['distortPerpSlowL']=neoprHorizDistortDict[n]['deltaMaxPerpSlowL']/eneto
    neoprHorizDistortDict[n]['checkDistortPerpSlowL'] = 'CUMPLE' if neoprHorizDistortDict[n]['distortPerpSlowL'] < slowL_distort_adm else 'NO CUMPLE'
    for cmb in mixLcombs2check:
        lstLC=cmb.replace(' ','').split('+')
        delta=abs(sum([dataRDict[lc]['disp'+dirPerp] for lc in lstLC]))
        if delta > neoprHorizDistortDict[n]['deltaMaxPerpMixL']:
            neoprHorizDistortDict[n]['deltaMaxPerpMixL']=delta
            neoprHorizDistortDict[n]['combDistortPerpMixL']=cmb
    neoprHorizDistortDict[n]['distortPerpMixL']=neoprHorizDistortDict[n]['deltaMaxPerpMixL']/eneto
    neoprHorizDistortDict[n]['checkDistortPerpMixL']='CUMPLE' if neoprHorizDistortDict[n]['distortPerpMixL'] < mixL_distort_adm else 'NO CUMPLE'
    
# Dump results
with open(outputFname,'w') as f:
    json.dump(neoprHorizDistortDict,f)
f.close()

