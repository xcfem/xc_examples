# Loads data
## Loads on each beam (half deck)
beamSW=5e3 # beam self-weigth [N/m]
slabSW=31.25e3 # concrete slab self-weigth [N/m]
deadL=1.6e3 # dead load [N/m]
qUnifTraffic=(9*3+2.5*2)*1e3 # uniform traffic load [N/m2]
QconcentrTraffic=800 # [kN]
lineWidth=3 # [m] width of each line
qTrfRest=2.5e3 #uniform traffic load on lines 2, 3 and rest [N/m2]

topTemp=+15 # degrees temperture at top face

epsShrinkage=-389e-6 #shrinkage strain
creepCoef=2.17 # creep coefficient

qUnifConstruct=1.2e3 # [N/m2] uniform load over the steel beam during construction
QconcentrConstruct=100e3 #[N] concentrated load over the steel beam during construction
