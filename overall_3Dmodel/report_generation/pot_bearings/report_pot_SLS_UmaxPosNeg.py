import os
import json
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import load_full_comb as lfc
import pot_report_functions as prf

# load combinations from which obtain maximum and minimum values
allELSdict=dict(lfc.ELSgrupo0)
allELSdict.update(lfc.ELSgrupo1)
allELSdict.update(lfc.ELSgrupo2)
allELSdict.update(lfc.ELSgrupo3)
allELSdict.update(lfc.ELSgrupo4)
allELSdict.update(lfc.ELSgrupo5)
combs=prf.combs_diasggr(allELSdict)

# read json file
resultFname=env.cfg.projectDirTree.getFullResultsPath()+'potBearing/pot_bearing_results.json'
if os.path.isfile(resultFname):
    f=open(resultFname,'r') # Open JSON file
    potResdict= json.load(f)
else:
    print('File '+resultFname+'does not exist')
    quit()
f.close()

dictDispMaxPosNeg=prf.gen_dict_DispMaxPosNeg(combs,potResdict)

texDir=env.cfg.projectDirTree.getFullReportPath()
texFileName=texDir+'pot_bearing_ELS_DispMaxPosNeg.tex'
texF=open(texFileName,'w') #
prf.gen_DispMaxPosNeg_table(texF,dictDispMaxPosNeg,caption='Apoyos POT. Valores de desplazamoentos máximos en combinaciones de ELS')
texF.close()


