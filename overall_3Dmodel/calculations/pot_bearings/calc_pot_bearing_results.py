# -*- coding: utf-8 -*-
''' Graba en el fichero 'pot_bearing_results.json' el diccionario potResdict con los resultados de esfuerzos y deformaciones obtenidos en cada caso de carga. La estructura del diccionario es la siguiente:
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
'''
            
import os
import json
from solution import predefined_solutions
from postprocess.config import default_config
import yaml
from pathlib import Path

# import local modules
import sys
workingDirectory= default_config.setWorkingDirectory()+'/' #search env_config.py
import xc_model as model #FE model generation
import pot_data as potD
import load_case_definition as LCdef
import data_material as datM
import env_config as env

# Json file with dictionary of results (resDict)
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'potBearing/pot_bearing_results.json'

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())


if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    potResdict= json.load(f)
else:
    potResdict=dict()
    for potId in potD.potData.keys():
        potResdict[potId]=dict()
        potElem=potD.potData[potId]['potElem']        
        potResdict[potId]['potDescr']=potD.potData[potId]['potDescr']
        potResdict[potId]['potDiam']=potElem.potMat.d
        potResdict[potId]['deltaFric']=potElem.potMat.deltaFrict
        potResdict[potId]['Kh']=potElem.potMat.getHorizontalStiffness()
        potResdict[potId]['LCres']=dict()
    with open(resultFname,'w') as f:
        json.dump(potResdict,f)
f.close()

# Cálculo
solProc= predefined_solutions.SimpleStaticLinear(FEcase)
solProc.setup()
analysis= solProc.analysis
for ky in LCdef.LCG_perm+LCdef.LCG_reol+ LCdef.LCG_vert + LCdef.LCG_fren +  LCdef.LCG_centr+ LCdef.LCG_lazo + LCdef.LCG_paseos + LCdef.LCG_viento+ LCdef.LCG_term:
    lcg=dictLCG[ky]
    lcName=lcg['LCname']
    lcDescr=lcg['description']
    model.modelSpace.removeAllLoadPatternsFromDomain()
    model.modelSpace.addLoadCaseToDomain(lcName)
    result= analysis.analyze(1)
    for potId in potD.potData.keys():
        potElem=potD.potData[potId]['potElem']
        potResdict[potId]['LCres'][lcName]=dict()
        potResdict[potId]['LCres'][lcName]['loadDescr']=lcDescr
        potResdict[potId]['LCres'][lcName]['Rx']=potElem.getMatXlocal().getStress()
        potResdict[potId]['LCres'][lcName]['Ry']=potElem.getMatYlocal().getStress()
        potResdict[potId]['LCres'][lcName]['Rz']=potElem.getMatZlocal().getStress()
        potResdict[potId]['LCres'][lcName]['dispX']=potElem.getMatXlocal().getStrain()
        potResdict[potId]['LCres'][lcName]['dispY']=potElem.getMatYlocal().getStrain()
        potResdict[potId]['LCres'][lcName]['dispZ']=potElem.getMatZlocal().getStrain()
        potResdict[potId]['LCres'][lcName]['rotX']=potElem.getMatTHXlocal().getStrain()
        potResdict[potId]['LCres'][lcName]['rotY']=potElem.getMatTHYlocal().getStrain()

    
# Dump the dictionary to json file
with open(resultFname,'w') as f:
    json.dump(potResdict,f)
f.close()
