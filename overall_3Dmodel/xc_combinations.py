from actions import combinations as cc

#    ***LIMIT STATE COMBINATIONS***
combContainer= cc.CombContainer()  #Container of load combinations

# COMBINATIONS OF ACTIONS FOR SERVICEABILITY LIMIT STATES
    # name:        name to identify the combination
    # rare:        combination for a rare design situation
    # freq:        combination for a frequent design situation
    # qp:          combination for a quasi-permanent design situation
    # earthquake:  combination for a seismic design situation
#Characteristic combinations.
combContainer.SLS.rare.add('ELSR01', '1.0*LS2')
#Frequent combinations.
combContainer.SLS.freq.add('ELSF01', '1.0*LS1')
#Quasi permanent combinations.
combContainer.SLS.qp.add('ELSQP01', '1.0*LS2')

# COMBINATIONS OF ACTIONS FOR ULTIMATE LIMIT STATES
    # name:        name to identify the combination
    # perm:        combination for a persistent or transient design situation
    # acc:         combination for a accidental design situation
    # fatigue:     combination for a fatigue design situation
    # earthquake:  combination for a seismic design situation
#Persistent and transitory situations.
combContainer.ULS.perm.add('ELU01', '1.2*LS1')
combContainer.ULS.perm.add('ELU02', '1.0*LS2')

#Fatigue.
# Combinations' names must be:
#        - ELUF0: unloaded structure (permanent loads)
#        - ELUF1: fatigue load in position 1.
combContainer.ULS.fatigue.add('ELUF0','1.00*GselfWeight+1.0*Qdecks')
combContainer.ULS.fatigue.add('ELUF1','1.00*GselfWeight+1.0*QearthPressWall')
