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
i=1
combContainer.SLS.rare.add('ELSR'+str(i), '1.0*LS2');i+=1
#Frequent combinations.
i=1
combContainer.SLS.freq.add('ELSF'+str(i), '1.0*LS1');i+=1
#Quasi permanent combinations.
i=1
combContainer.SLS.qp.add('ELSQP'+str(i), '1.0*LS2');i+=1

# COMBINATIONS OF ACTIONS FOR ULTIMATE LIMIT STATES
    # name:        name to identify the combination
    # perm:        combination for a persistent or transient design situation
    # acc:         combination for a accidental design situation
    # fatigue:     combination for a fatigue design situation
    # earthquake:  combination for a seismic design situation
#Persistent and transitory situations.
i=1
combContainer.ULS.perm.add('ELU'+str(i), '1.2*LS1');i+=1
combContainer.ULS.perm.add('ELU'+str(i), '1.0*LS2');i+=1

#Fatigue.
# Combinations' names must be:
#        - ELUF0: unloaded structure (permanent loads)
#        - ELUF1: fatigue load in position 1.
i=1
combContainer.ULS.fatigue.add('ELUF'+str(i),'1.00*GselfWeight+1.0*Qdecks');i+=1
combContainer.ULS.fatigue.add('ELUF'+str(i),'1.00*GselfWeight+1.0*QearthPressWall');i+=1
