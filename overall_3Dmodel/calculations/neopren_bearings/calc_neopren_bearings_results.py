# -*- coding: utf-8 -*-
''' Graba en el fichero 'neopren_bearing_results.json' el diccionario neoprResdict con los resultados de esfuerzos y deformaciones obtenidos en cada caso de carga. La estructura del diccionario es la siguiente:
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
'''
            
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
import xc_model as model #FE model generation
import load_case_definition as LCdef
import data_material as datM
import env_config as env
# Json file with dictionary of results (resDict)
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'neopBearing/neopren_bearing_results.json'

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())

if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    neoprResdict= json.load(f)
else:
    neoprResdict=dict()
    for n in model.listIdBearEl:
        nId=n[0]
        v,nvig=nId.split('_')
        port='Este' if 'E' in v else 'Oeste' 
        nDescr='Viga '+str(nvig)+' pórtico '+port
        neoprResdict[nId]=dict()
        neoprResdict[nId]['neopDescr']=nDescr
        neoprResdict[nId]['neopDim']=n[2]
        neoprResdict[nId]['LCres']=dict()
    with open(resultFname,'w') as f:
        json.dump(neoprResdict,f)
f.close()

# Cálculo
analysis= predefined_solutions.simple_static_linear(model.FEcase)
#for ky in LCdef.LCG_perm+LCdef.LCG_reol:
#for  ky in LCdef.LCG_vert:
#for  ky in LCdef.LCG_fren:
#for  ky in LCdef.LCG_centr:
#for  ky in (LCdef.LCG_lazo + LCdef.LCG_paseos + LCdef.LCG_viento):
for  ky in LCdef.LCG_term:
    lcg=dictLCG[ky]
    lcName=lcg['LCname']
    lcDescr=lcg['description']
    model.modelSpace.removeAllLoadPatternsFromDomain()
    model.modelSpace.addLoadCaseToDomain(lcName)
    result= analysis.analyze(1)
    for n in model.listIdBearEl:
        nId=n[0]
        nElem=n[1]
        neoprResdict[nId]['LCres'][lcName]=dict()
        neoprResdict[nId]['LCres'][lcName]['loadDescr']=lcDescr
        neoprResdict[nId]['LCres'][lcName]['Rx']=nElem.getMaterials()[0].getStress()
        neoprResdict[nId]['LCres'][lcName]['Ry']=nElem.getMaterials()[1].getStress()
        neoprResdict[nId]['LCres'][lcName]['Rz']=nElem.getMaterials()[2].getStress()
        neoprResdict[nId]['LCres'][lcName]['Mx']=nElem.getMaterials()[3].getStress()
        neoprResdict[nId]['LCres'][lcName]['My']=nElem.getMaterials()[4].getStress()
        neoprResdict[nId]['LCres'][lcName]['Mz']=nElem.getMaterials()[5].getStress()
        neoprResdict[nId]['LCres'][lcName]['dispX']=nElem.getMaterials()[0].getStrain()
        neoprResdict[nId]['LCres'][lcName]['dispY']=nElem.getMaterials()[1].getStrain()
        neoprResdict[nId]['LCres'][lcName]['dispZ']=nElem.getMaterials()[2].getStrain()
        neoprResdict[nId]['LCres'][lcName]['rotX']=nElem.getMaterials()[3].getStrain()
        neoprResdict[nId]['LCres'][lcName]['rotY']=nElem.getMaterials()[4].getStrain()
        neoprResdict[nId]['LCres'][lcName]['rotZ']=nElem.getMaterials()[5].getStrain()
    
# Dump the dictionary to json file
with open(resultFname,'w') as f:
    json.dump(neoprResdict,f)
f.close()
