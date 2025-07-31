from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import data_geom as datG

# Loads data
## Loads on each beam (half deck)
deadL=1.6e3 # dead load [N/m2]
qUnifTraffic=(9*3+2.5*(datG.slabW-3))*1e3/datG.slabW # uniform traffic load [N/m2]
# heavy vehicle concentrated loads (the sum is 800 kN = half bridge)
import geom
from actions.roadway_traffic import load_model_base as lmb
# wheels
w1=lmb.WheelLoad(pos=geom.Pos2d(-1,-0.6),ld=150e3,lx=0.4,ly=0.4)
w2=lmb.WheelLoad(pos=geom.Pos2d(+1,-0.6),ld=150e3,lx=0.4,ly=0.4)
w3=lmb.WheelLoad(pos=geom.Pos2d(-1,+0.6),ld=150e3,lx=0.4,ly=0.4)
w4=lmb.WheelLoad(pos=geom.Pos2d(+1,+0.6),ld=150e3,lx=0.4,ly=0.4)
w5=lmb.WheelLoad(pos=geom.Pos2d(+2,-0.6),ld=100e3,lx=0.4,ly=0.4)
w6=lmb.WheelLoad(pos=geom.Pos2d(+2,+0.6),ld=100e3,lx=0.4,ly=0.4)
truck3axes=lmb.LoadModel(wLoads=[w1,w2,w3,w4,w5,w6])

#QconcentrTraffic=800 # [kN]
laneWidth=3 # [m] width of each lane
qTrfRest=2.5e3 #uniform traffic load on lines 2, 3 and rest [N/m2]
# Rheologic actions
epsShrinkage_inf=-389e-6 #shrinkage strain (t=infinity)
epsShrinkage_15=-51.5e-6
creepCoef=2.17 # creep coefficient

qUnifConstruct=1.2e3 # [N/m2] uniform load over the steel beam during construction
QconcentrConstruct=100e3 #[N] concentrated load over the steel beam during construction

# Thermal action
## according to m-10 ACHE monograph
# TempIncr=+15 # degrees temperature for thermal increment
# TempDecr=-18 # degrees temperature for thermal decrement
## according to AN-UNE-EN 1991-1-5, art. 6.1.4.2
TempIncr=+18 # [degrees] temperature of steel beam for thermal increment
TempDecr=-10 # [degree]s temperature of steel beam for thermal decrement

## ARTICLE  6.1.4.2 AN-UNE-EN 1991-1-5:
# Para tableros mixtos (Tipo 2), se debe aplicar lo siguiente:
# En las condiciones de calentamiento (“heating”), en las que se origina una ganancia de calor de las secciones parciales de acero respecto de las de hormigón, se aplica a la sección parcial de acero un incremento diferencial de ∆TM,heat = +18 °C, respecto de las secciones parciales de hormigón (ya sea losa superior u hormigón de fondo).
# En las condiciones de enfriamiento (“cooling”), en las que se produce una pérdida de calor de las secciones de acero respecto de las secciones parciales de hormigón
