import os
import json
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import load_full_comb as lfc
import pot_report_functions as prf

# load combinations from which obtain maximum and minimum values
allELUdict=dict(lfc.ELUgrupo0)
allELUdict.update(lfc.ELUgrupo1)
allELUdict.update(lfc.ELUgrupo2)
allELUdict.update(lfc.ELUgrupo3)
allELUdict.update(lfc.ELUgrupo4)
allELUdict.update(lfc.ELUgrupo5)
combs=prf.combs_diasggr(allELUdict)

# read json file
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'potBearing/pot_bearing_results.json'
if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    potResdict= json.load(f)
else:
    print('File '+resultFname+'does not exist')
    quit()
f.close()

dictRmaxmin=prf.gen_dict_Rmaxmin(combs,potResdict)

texDir=env.cfg.projectDirTree.getFullReportPath()
texFileName=texDir+'pot_bearing_ELU_Rmaxmin.tex'
texF=open(texFileName,'w') #
prf.gen_Rmaxmin_table(texF,dictRmaxmin,caption='Apoyos POT. Valores de carga máximos y mínimos en combinaciones de ELU')
texF.close()


