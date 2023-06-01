# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import json
import sys
from postprocess import limit_state_data as lsd
from postprocess.config import default_config
from postprocess.reports import common_formats as fmt


class NeoprenePad(object):
    ''' Check strength and performance of bridge neoprene pad.

     :ivar a: length (longitudinal dimension) of the bearing
     :ivar b: width (transversal dimension) of the bearing
     :ivar E: elastic modulus of the elastomeric material
     :ivar G: shear modulus of the elastomeric material
     :ivar n_layers: number of neoprene layers in each bearing
     :ivar t_layer: thickness of each neoprene layer
    '''
    def __init__(self, a:float, b:float, E: float, G: float, n_layers:int, t_layer:float):
        ''' Constructor.
         :param a: length (longitudinal dimension) of the bearing
         :param b: width (transversal dimension) of the bearing
         :param E: elastic modulus of the elastomeric material
         :param G: shear modulus of the elastomeric material
         :param n_layers: number of neoprene layers in each bearing
         :param t_layer: thickness of each neoprene layer
        '''
        self.a= a
        self.b= b
        self.E= E
        self.G= G
        self.n_layers= n_layers
        self.t_layer= t_layer

    def checkMinimumVerticalPressure(self, reactions):
        ''' Check the minimum vertical pressure on the bearing pad.

        :param reactions: loads on the bearing pad.
        '''
        minFz= 6.023e23
        minFzComb= None
        for combName in reactions:
            nodes= reactions[combName]
            for n in nodes:
                nodeReactions= nodes[n]['reactions']
                Fz= nodeReactions['Fz']
                if(Fz<minFz):
                    minFz= Fz
                    minFzComb= combName
        minVerticalPressure= minFz/self.a/self.b
        return minVerticalPressure, minFz, minFzComb
    
    def checkMaximumVerticalPressure(self, reactions):
        ''' Check the maximum vertical pressure on the bearing pad.

        :param reactions: loads on the bearing pad.
        '''
        maxFz= -6.023e23
        maxFzComb= None
        for combName in reactions:
            nodes= reactions[combName]
            for n in nodes:
                nodeReactions= nodes[n]['reactions']
                Fz= nodeReactions['Fz']
                if(Fz>maxFz):
                    maxFz= Fz
                    maxFzComb= combName
        maxVerticalPressure= maxFz/self.a/self.b
        return maxVerticalPressure, maxFz, maxFzComb
    
    def checkMaximumDistortion(self, reactions, longitudinalComponent= 'Fx'):
        ''' Check the maximum distortion on the bearing pad.

        :param reactions: loads on the bearing pad.
        :param longitudinalComponent: longitudinal component of the reaction.
        '''
        maxFx= -6.023e23
        minFx= -maxFx
        maxFxComb= None
        minFxComb= None
        for combName in reactions:
            nodes= reactions[combName]
            for n in nodes:
                nodeReactions= nodes[n]['reactions']
                Fx= nodeReactions[longitudinalComponent]
                if(Fx>maxFx):
                    maxFx= Fx
                    maxFxComb= combName
                if(Fx<minFx):
                    minFx= Fx
                    minFxComb= combName
        if(maxFx>abs(minFx)):
            H= maxFx # Maximum horizontal reaction.
            maxDistortionComb= maxFxComb
        else:
            H= minFx # Minimum horizontal reaction.
            maxDistortionComb= minFxComb
        tau= H/self.a/self.b
        hNetNeopr= self.n_layers*self.t_layer
        maxDistortion= tau/self.G
        horizontalDisplacement= H/self.G/self.a/self.b*hNetNeopr
        return maxDistortion, horizontalDisplacement, maxDistortionComb

    def report(self, ulsReactions, freqReactions, qpermReactions, os= sys.stdout):
        ''' Get a report of the checking results.

        :param os: output stream.
        '''
        minVerticalPressure, minFz, minFzComb= self.checkMinimumVerticalPressure(qpermReactions)
        os.write( "\\noindent \\underline{Tensión vertical mínima:}\\\\\n")
        os.write( 'Combinación: '+minFzComb+'\n')
        os.write( 'Reacción: $'+fmt.Esf.format(minFz/1e3)+'\ kN$\n')
        os.write( '$\sigma_{z,min} = '+ fmt.Stress.format(minVerticalPressure/1e6) + '\ MPa$\n')
        if minVerticalPressure >= 3e6:
            os.write( '$\\sigma_{z,min} \\ge 3 MPa \\rightarrow OK $\n' )
        else:
            os.write( '$\\sigma_{z,min} < 3 MPa \\rightarrow anclaje $\n' )
            
        maxVerticalPressure, maxFz, maxFzComb= self.checkMaximumVerticalPressure(ulsReactions)
        os.write( "\\noindent \\underline{Tensión vertical máxima:}\\\\\n")
        os.write( 'Combinación: '+maxFzComb+'\n')
        os.write( 'Reacción: $'+fmt.Esf.format(maxFz/1e3)+'\ kN$\n')
        os.write( '$\sigma_{z,max} = '+ fmt.Stress.format(maxVerticalPressure/1e6) + '\ MPa$\n')
        if maxVerticalPressure <= 15e6:
            os.write( '$\\sigma_{z,max} \\le 15 MPa \\rightarrow OK $\n' )
        else:
            os.write( '$\\sigma_{z,max} < 15 MPa \\rightarrow KO $\n' )
        # Maximum distortion under short term loads 
        maxDistortion, horizontalDisplacement, maxDistortionComb= self.checkMaximumDistortion(freqReactions, longitudinalComponent= 'Fx')
        os.write( "\\underline{Distorsión máxima por cargas de corta duración:}\\\\\n")
        os.write( 'Combinación: '+maxDistortionComb+'\n')
        os.write( '$u_{x,max} = '+ fmt.Displacement.format(horizontalDisplacement*1e3) + ' mm$\n')
        if maxDistortion <= 0.7:
            os.write( '$Distors. = \\cfrac{u_{x,max}}{e_{neto}} = ' + fmt.Length.format(maxDistortion) + ' \\le 0.7 \\rightarrow OK $\n' )
        else:
            os.write( '$Distors. = \\cfrac{u_{x,max}}{e_{neto}} = ' + fmt.Length.format(maxDistortion) + ' \\gt 0.7 \\rightarrow KO $\n' )
        # Maximum distortion under long term loads 
        maxDistortion, horizontalDisplacement, maxDistortionComb= self.checkMaximumDistortion(qpermReactions, longitudinalComponent= 'Fx')
        os.write( "\\underline{Distorsión máxima por cargas lentas:}\\\\\n")
        os.write( 'Combinación: '+maxDistortionComb+'\n')
        os.write( '$u_{x,max} = '+ fmt.Displacement.format(horizontalDisplacement*1e3) + ' mm$\n')
        if maxDistortion <= 0.5:
            os.write( '$Distors. = \\cfrac{u_{x,max}}{e_{neto}} = ' + fmt.Length.format(maxDistortion) + ' \\le 0.5 \\rightarrow OK $\n' )
        else:
            os.write( '$Distors. = \\cfrac{u_{x,max}}{e_{neto}} = ' + fmt.Length.format(maxDistortion) + ' \\gt 0.5 \\rightarrow KO $\n' )



exec(default_config.compileCode('../xc_model.py'))
print('model built')
# Load combinations
exec(cfg.compileCode('load_combinations.py'))

ulsReactionsFileName= cfg.projectDirTree.getReactionsResultsPath()+'reactions_ULS_normalStressesResistance.json' # Specific bearing pads freqReactions needed.
ulsReactionsFile= cfg.open(ulsReactionsFileName, mode= 'r')
ulsReactionsDict= json.load(ulsReactionsFile)
ulsReactionsFile.close()

freqReactionsFileName= cfg.projectDirTree.getReactionsResultsPath()+'reactions_SLS_frequentLoadsCrackControl.json' # Specific bearing pads reactions needed.
freqReactionsFile= cfg.open(freqReactionsFileName, mode= 'r')
freqReactionsDict= json.load(freqReactionsFile)
freqReactionsFile.close()

qpermReactionsFileName= cfg.projectDirTree.getReactionsResultsPath()+'reactions_SLS_quasiPermanentLoadsLoadsCrackControl.json' # Specific bearing pads freqReactions needed.
qpermReactionsFile= cfg.open(qpermReactionsFileName, mode= 'r')
qpermReactionsDict= json.load(qpermReactionsFile)
qpermReactionsFile.close()

neoprenePad= NeoprenePad(a= 0.50, b= 0.60, E= 600e6, G= 0.8e6, n_layers= 5, t_layer= 8e-3)

neoprenePad.report(ulsReactionsDict, freqReactionsDict, qpermReactionsDict)

