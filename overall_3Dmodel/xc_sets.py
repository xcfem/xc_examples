from model.sets import sets_mng as setMng
from model.geometry import geom_utils as gut

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
# import local modules
import env_config as env
import xc_init
import data_geom as datG
import xc_geom as xcG # geometry data
import xc_fem as xcF # import this module for future displays and calculations, since xc_sets is imported as a general rule.

# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep

# Sets 
decklv1Set=xcG.decklv1 ; decklv1Set.description='Deck level 1' ; decklv1Set.color=env.cfg.colors['purple01']

decklv2Set=xcG.decklv2 ; decklv2Set.description='Deck level 2' ; decklv2Set.color=env.cfg.colors['blue01']

steelPlateSet=xcG.steelPlate; steelPlateSet.description='Steel plate' ; steelPlateSet.color=env.cfg.colors['blue02']

footSet=xcG.foot ; footSet.description='Foundation' ; footSet.color=env.cfg.colors['orange01']

wallSet=xcG.wall ; wallSet.description='Wall' ; wallSet.color=env.cfg.colors['green01']

beamXconcrSet=xcG.beamXconcr ; beamXconcrSet.description='Beams in X direction' ; beamXconcrSet.color=env.cfg.colors['blue03']

beamYSet=xcG.beamY ; beamYSet.description='Beams in Y direction' ; beamYSet.color=env.cfg.colors['green03']

columnZconcrSet=xcG.columnZconcr ; columnZconcrSet.description='Concrete columns' ; columnZconcrSet.color=env.cfg.colors['red03']

columnZsteelSet=xcG.columnZsteel ; columnZsteelSet.description='Steel columns' ; columnZsteelSet.color=env.cfg.colors['blue02']

beamXsteelSet=xcG.beamXsteel

beamsSet=modelSpace.setSum('beamsSet',[beamXconcrSet,beamYSet]) ; beamsSet.description='Beams' ; beamsSet.fillDownwards()
#out.displayBlocks()

lstSets=[decklv1Set,decklv2Set,footSet,wallSet,beamXconcrSet,beamYSet,columnZconcrSet,columnZsteelSet]

decksSet=modelSpace.setSum('decksSet',[decklv1Set,decklv2Set]) ; decksSet.description='Decks' ; decksSet.color=env.cfg.colors['purple01'] ; decksSet.fillDownwards()

allShellsSet=modelSpace.setSum('allShellsSet',[decklv1Set,decklv2Set,footSet,wallSet,steelPlateSet]) ; allShellsSet.description='Shell elements' ; allShellsSet.fillDownwards()

allBeamsSet=modelSpace.setSum('allBeamsSet',[beamXconcrSet,beamXsteelSet,beamYSet,columnZconcrSet,columnZsteelSet]) ; allBeamsSet.description='Beams+columns' ; allBeamsSet.fillDownwards()

overallSet=modelSpace.setSum('overallSet',[beamXconcrSet,beamXsteelSet,beamYSet,columnZconcrSet,columnZsteelSet,wallSet,footSet,decklv1Set,decklv2Set,steelPlateSet]) ; overallSet.description='overall set' ; overallSet.color=env.cfg.colors['purple01'] ; overallSet.fillDownwards()

allConcreteSet=modelSpace.setSum('allConcreteSet',[beamXconcrSet,beamYSet,columnZconcrSet,wallSet,footSet,decklv1Set,decklv2Set]) ; allConcreteSet.description='concrete elements'; allConcreteSet.fillDownwards()

beamXSet=modelSpace.setSum('beamXSet',[beamXconcrSet,beamXsteelSet]) ; beamXSet.description='beams X' ; beamXSet.fillDownwards()

columnZSet=modelSpace.setSum('columnZSet',[columnZconcrSet,columnZsteelSet]) ; columnZSet.description='columns' ; columnZSet.fillDownwards()

allSteelSet=modelSpace.setSum('allSteelSet',[beamXsteelSet,columnZsteelSet,steelPlateSet]) ; allSteelSet.description='steel elements' ; allSteelSet.fillDownwards()

mixSet=modelSpace.setSum('mixSet',[wallSet,columnZconcrSet]) ; mixSet.fillDownwards()
#sets for displaying some results
pBase=gut.rect2DPolygon(xCent=datG.LbeamX/2.,yCent=0,Lx=datG.LbeamX,Ly=datG.LbeamY-1.0)

allShellsResSet=setMng.set_included_in_orthoPrism(preprocessor=prep,setInit=allShellsSet,prismBase=pBase,prismAxis='Z',setName='allShellsResSet')
 
prep.getSets.getSet('total').fillDownwards()


