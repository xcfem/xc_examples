from actions import load_cases as lcases

i=1
for lc in [trainLoadModel]:
    auxLC=lcases.LoadCase(preprocessor=prep,name=lc.name+str(i),loadPType="default",timeSType="constant_ts")
    auxLC.create()
    auxLC.addLstLoads([lc])
    modelSpace.addLoadCaseToDomain(auxLC.name)
    out.displayLoads()
    i+=1
    modelSpace.removeAllLoadPatternsFromDomain()

    
model.modelSpace.addLoadCaseToDomain(Q2A2.name)
model.out.displayLoads()
model.modelSpace.removeAllLoadPatternsFromDomain()
