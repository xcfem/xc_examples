from model.sets import sets_mng as setMng
from model.geometry import geom_utils as gut

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
# import local modules
import env_config as env
import xc_init
import xc_geom as xcG # geometry data
#import xc_fem_beam as xcFb # import this module for future displays and calculations, since xc_sets is imported as a general rule.
# Common variables
import xc_fem_beam as xcFb
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep

beamST1=modelSpace.setSum('beamT1',[xcG.tfST1,xcG.bfST1,xcG.wST1]); beamST1.description='Viga sección tipo 1'; beamST1.fillDownwards(); beamST1.color=env.cfg.colors['purple01']
beamST2=modelSpace.setSum('beamT2',[xcG.tfST2,xcG.bfST2,xcG.wST2]); beamST2.description='Viga sección tipo 2'; beamST2.fillDownwards(); beamST2.color=env.cfg.colors['blue02']
beamST3=modelSpace.setSum('beamT3',[xcG.tfST3,xcG.bfST3,xcG.wST3]); beamST3.description='Viga sección tipo 3'; beamST3.fillDownwards(); beamST3.color=env.cfg.colors['red01']

bottomFlange=modelSpace.setSum('bottomFlange',[xcG.bfST1,xcG.bfST2,xcG.bfST3]);bottomFlange.description='Ala inferior';  bottomFlange.fillDownwards()
topFlange=modelSpace.setSum('topFlange',[xcG.tfST1,xcG.tfST2,xcG.tfST3]);topFlange.description='Ala superior';  topFlange.fillDownwards()
web=modelSpace.setSum('web',[xcG.wST1,xcG.wST2,xcG.wST3]);web.description='Ala superior';  web.fillDownwards()
#out.displayFEMesh([beamST1,beamST2,beamST3])
beam=modelSpace.setSum('beam',[beamST1,beamST2,beamST3]); beam.description='Viga metálica'; beam.fillDownwards(); beam.color=env.cfg.colors['red01']
#out.displayFEMesh(beam)

slab=xcG.slab; slab.description='Losa de horm.'; slab.fillDownwards(); slab.color=env.cfg.colors['purple01']

shearC=xcG.shearC; shearC.description='Shear connections'; shearC.fillDownwards()
