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

if os.path.isfile(inputFname):
    f=open(inputFname,'r') # Open JSON file
    neoprDatasdict= json.load(f)
else:
    print("Can't find file:',inputFname")
    quit()

f.close()

for i in range(30,32+1):
    neoprDatasdict['VW_'+str(i)]['neopDim']='200x250x21'
for i in range(32,37+1):
    neoprDatasdict['VE_'+str(i)]['neopDim']='200x400x21'
for i in range(15,19+1):
    neoprDatasdict['VE_'+str(i)]['neopDim']='200x400x21'
for i in range(7,8+1):
    neoprDatasdict['VW_'+str(i)]['neopDim']='200x400x21'

# Dump results
with open(inputFname,'w') as f:
    json.dump(neoprDatasdict,f)
f.close()
