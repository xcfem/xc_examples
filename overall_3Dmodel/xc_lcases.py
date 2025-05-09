
from actions import load_cases as lcases

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_geom as xcG
import xc_loads as xcL
import xc_roadway_loads  as xcLr
import xc_sets

# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep

GselfWeight=lcases.LoadCase(preprocessor=prep,name="GselfWeight",loadPType="default",timeSType="constant_ts")
GselfWeight.create()
GselfWeight.addLstLoads([xcL.selfWeight])
'''
# display
modelSpace.addLoadCaseToDomain("GselfWeight")
out.displayLoads()
modelSpace.removeLoadCaseFromDomain("GselfWeight")
'''
# self-weight direct generation
'''
selfWeight=modelSpace.newLoadPattern(name="selfWeight",lpType="default")
modelSpace.setCurrentLoadPattern(selfWeight.name)
for e in stem.elements: e.createInertiaLoad(grav)
for e in lintel.elements: e.createInertiaLoad(grav)
modelSpace.addLoadCaseToDomain(selfWeight.name) # añadirla al dominio antes de dibujarla
'''

Qdecks=lcases.LoadCase(preprocessor=prep,name="Qdecks")
Qdecks.create()
Qdecks.addLstLoads([xcL.unifLoadDeck1,xcL.unifLoadDeck2])

QearthPressWall=lcases.LoadCase(preprocessor=prep,name="QearthPressWall",loadPType="default",timeSType="constant_ts")
QearthPressWall.create()
QearthPressWall.addLstLoads([xcL.earthPressLoadWall])

QearthPWallStrL=lcases.LoadCase(preprocessor=prep,name="QearthPWallStrL",loadPType="default",timeSType="constant_ts")
QearthPWallStrL.create()
QearthPWallStrL.addLstLoads([xcL.earthPWallStrL])

QearthPWallLinL=lcases.LoadCase(preprocessor=prep,name="QearthPWallLinL",loadPType="default",timeSType="constant_ts")
QearthPWallLinL.create()    
QearthPWallLinL.addLstLoads([xcL.earthPWallLinL])

QearthPWallHrzL=lcases.LoadCase(preprocessor=prep,name="QearthPWallHrzL",loadPType="default",timeSType="constant_ts")
QearthPWallHrzL.create()
QearthPWallHrzL.addLstLoads([xcL.earthPWallHrzL])

qunifBeams=lcases.LoadCase(preprocessor=prep,name="qunifBeams",loadPType="default",timeSType="constant_ts")
qunifBeams.create()
qunifBeams.addLstLoads([xcL.unifLoadBeamsY])
'''
modelSpace.addLoadCaseToDomain("datL.qunifBeams")
out.displayLoads(beams)
modelSpace.removeLoadCaseFromDomain("datL.qunifBeams")
'''

QpntBeams=lcases.LoadCase(preprocessor=prep,name="QpntBeams",loadPType="default",timeSType="constant_ts")
QpntBeams.create()
QpntBeams.addLstLoads([xcL.QpuntBeams])

qlinDeck=lcases.LoadCase(preprocessor=prep,name="qlinDeck",loadPType="default",timeSType="constant_ts")
qlinDeck.create()
qlinDeck.addLstLoads([xcL.unifLoadLinDeck2])

QwheelDeck1=lcases.LoadCase(preprocessor=prep,name="QwheelDeck1",loadPType="default",timeSType="constant_ts")
QwheelDeck1.create()
QwheelDeck1.addLstLoads([xcL.wheelDeck1])

QvehicleDeck1=lcases.LoadCase(preprocessor=prep,name="QvehicleDeck1",loadPType="default",timeSType="constant_ts")
QvehicleDeck1.create()
QvehicleDeck1.addLstLoads([xcLr.vehicleDeck1])

LS1=lcases.LoadCase(preprocessor=prep,name="LS1",loadPType="default",timeSType="constant_ts")
LS1.create()
LS1.addLstLoads([xcL.selfWeight,xcL.unifLoadDeck1,xcL.unifLoadDeck2,xcL.earthPressLoadWall,xcL.earthPWallStrL,xcL.earthPWallLinL])



LS2=lcases.LoadCase(preprocessor=prep,name="LS2",loadPType="default",timeSType="constant_ts")
LS2.create()
LS2.addLstLoads([xcL.selfWeight,xcL.earthPWallHrzL,xcL.unifLoadBeamsY,xcL.QpuntBeams,xcL.unifLoadLinDeck2,xcL.wheelDeck1])

'''
for lc in [LS1,LS2]:
    modelSpace.addLoadCaseToDomain(lc.name)
    out.displayLoads()
    modelSpace.removeLoadCaseFromDomain(lc.name)
'''
'''
from solution import predefined_solutions
solProc= predefined_solutions.SimpleStaticLinear(FEcase)
solProc.setup()
analysis= solProc.analysis
for lc in [LS1,LS2]:
    modelSpace.removeAllLoadPatternsFromDomain()
    modelSpace.addLoadCaseToDomain(lc.name)
    result= analysis.analyze(1)
    out.displayDispRot('uZ')
    modelSpace.removeLoadCaseFromDomain(lc.name)
'''
lstLC=[GselfWeight,Qdecks,QearthPressWall,QearthPWallStrL,QearthPWallLinL,QearthPWallHrzL,qunifBeams,QpntBeams,qlinDeck,QwheelDeck1,QvehicleDeck1,LS1,LS2]

#Shrinkage
Gshrink=lcases.LoadCase(preprocessor=prep,name="Gshrink",loadPType="default",timeSType="constant_ts")
Gshrink.create()
modelSpace.setCurrentLoadPattern(Gshrink.name)
Gshrink.addLstLoads([xcL.shrinkage])

