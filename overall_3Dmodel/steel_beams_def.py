from materials.ec3 import EC3Beam as ec3b
from materials.ec3 import EC3_limit_state_checking as EC3lsc
from postprocess.config import default_config
from model.geometry import grid_model as gm

# local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import model_gen as model

# ** Steel beams
# Support coefficients (1==free, 0.5==prevented) (all default to 1)
# ky: lateral bending, kw: warping, k1: warping and lateral bending at left
# end, k2:  warping and lateral bending at right end

supCf_free=EC3lsc.BeamSupportCoefficients(ky=1.0,kw=1.0,k1=1.0,k2=1.0)
supCf=EC3lsc.BeamSupportCoefficients(ky=1.0,kw=1.0,k1=0.5,k2=1.0)

# Columns definition
col01a_ln=model.gridGeom.getLstLinRange(gm.IJKRange((0,model.lastYpos,0),(0,model.lastYpos,1)))
col01a=ec3b.EC3Beam(name='col01a',ec3Shape=model.columnZsteel_mat,beamSupportCoefs=supCf_free,lstLines=col01a_ln)
col01a.setControlPoints()
col01a.installULSControlRecorder(recorderType="element_prop_recorder")

col01b_ln=model.gridGeom.getLstLinRange(gm.IJKRange((0,model.lastYpos,1),(0,model.lastYpos,model.lastZpos)))
col01b=ec3b.EC3Beam(name='col01b',ec3Shape=model.columnZsteel_mat,beamSupportCoefs=supCf_free,lstLines=col01b_ln)
col01b.setControlPoints()
col01b.installULSControlRecorder(recorderType="element_prop_recorder")

col02a_pnt=model.gridGeom.getLstPntRange(gm.IJKRange((model.lastXpos,model.lastYpos,0),(model.lastXpos,model.lastYpos,1)))
col02a=ec3b.EC3Beam(name='col02a',ec3Shape=model.columnZsteel_mat,beamSupportCoefs=supCf_free,lstPoints=col02a_pnt)
col02a.setControlPoints()
col02a.installULSControlRecorder(recorderType="element_prop_recorder")

col02b_pnt=model.gridGeom.getLstPntRange(gm.IJKRange((model.lastXpos,model.lastYpos,1),(model.lastXpos,model.lastYpos,model.lastZpos)))
col02b=ec3b.EC3Beam(name='col02b',ec3Shape=model.columnZsteel_mat,beamSupportCoefs=supCf_free,lstPoints=col02b_pnt)
col02b.setControlPoints()
col02b.installULSControlRecorder(recorderType="element_prop_recorder")

col03_ln=model.gridGeom.getLstLinRange(gm.IJKRange((1,model.lastYpos,0),(1,model.lastYpos,1)))
col03=ec3b.EC3Beam(name='col03',ec3Shape=model.columnZsteel_mat,beamSupportCoefs=supCf,lstLines=col03_ln)
col03.setControlPoints()
col03.installULSControlRecorder(recorderType="element_prop_recorder")

#X beam definition
beam01_pnt=model.gridGeom.getLstPntRange(model.beamXsteel_rg)
beam01=ec3b.EC3Beam(name='beam01',ec3Shape=model.beamXsteel_mat,beamSupportCoefs=supCf_free,lstPoints=beam01_pnt)
beam01.setControlPoints()
beam01.installULSControlRecorder(recorderType="element_prop_recorder")

