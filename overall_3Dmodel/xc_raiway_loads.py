import data_rail as datR
# railway traffic
xaxis=0
yminAxis=0; ymaxAxis=10
zSlab=5
Hrail=datR.slabTh/2.+datR.thBallast+datR.sleeperHeight
polyAxisvert=[geom.Pos3d(xaxis,yminAxis,zSlab+Hrail),geom.Pos3d(xaxis,ymaxAxis,zSlab+Hrail)]
polyAxis=geom.Polyline3d(polyAxisvert)

from actions.railway_traffic import EC1_rail_load_models
trackAxis= EC1_rail_load_models.TrackAxis(trackAxis= polyAxis)
locomotiveLM1= EC1_rail_load_models.get_locomotive_LM1()
trainLoadModel= EC1_rail_load_models.TrainLoadModel(locomotive= locomotiveLM1, uniformLoad= datR.qunifUIC71, dynamicFactor= datR.coefImp, classificationFactor= datR.coefClasif)
spreadingLayers=[[datR.sleeperHeight,datR.sleeperSpreadToDepthRatio],
                 [datR.thBallast,datR.ballastSpreadToDepthRatio]]

## Q2A: Componentes verticales UIC71
### Posición 1
Q2A1=lcases.LoadCase(preprocessor=prep,name="Q2A1",loadPType="default",timeSType="constant_ts")
Q2A1.create()
modelSpace.setCurrentLoadPattern(Q2A1.name)
nodalLoads= trackAxis.defDeckLoadsThroughLayers(trainModel= trainLoadModel, relativePosition= 0.2, spreadingLayers= spreadingLayers, deckThickness= datR.slabTh, deckSpreadingRatio= 1/1, originSet= topSlab)
