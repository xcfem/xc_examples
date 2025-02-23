# -*- coding: utf-8 -*-
''' Utilities for the generation of strut-and-tie models.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis Claudio Pérez Tato (LCPT)"
__copyright__= "Copyright 2025, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

from model.mesh import strut_and_tie_utils
import uuid
import geom
import xc

class Pilecap3Piles(object):
    def __init__(self, pierBottomNode, pileTopNodeA, pileTopNodeB, pileTopNodeC, pierEffectiveDiameter):
        ''' Constructor.

        :param pierBottomNode: bottom node of the pier.
        :param pileTopNodeA: top node of the first pile.
        :param pileTopNodeB: top node of the second pile.
        :param pileTopNodeC: top node of the third pile.
        :param pierEffectiveDiameter: effective diameter of the pier.
        '''
        self.pierBottomNode= pierBottomNode
        self.pileTopNodeA= pileTopNodeA
        self.pileTopNodeB= pileTopNodeB
        self.pileTopNodeC= pileTopNodeC
        self.pierEffectiveDiameter= pierEffectiveDiameter
        

    def createStrutAndTieModel(self, modelSpace, strutArea, concrete, pileTiesArea, radialTiesArea, bottomChordsTiesArea, topChordsTiesArea, shearTiesArea, reinfSteel, xcPierSectionMaterial, linearElastic= False):
        ''' Creates an strut-and-tie model and attach it to the nodes of the 
            pier and the piles.

        :param modelSpace: PredefinedSpace object used to create the FE model.
        :param strutAre: area of the struts.
        :param concrete: concrete material.
        :param pileTiesArea: vertical ties over each pile.
        :param radialTiesArea= area of the radial ties joining the pier and 
                               the piles.
        :param bottomChordTiesArea= area of the ties joining the heads of the
                                    piles. 
        :param topChordTiesArea= area of the ties joining the tips of the 
                                 vertical ties on each pile.
        :param shearTiesArea: area of the vertical ties between piles.
        :param reinfSteel: reinforcing steel material.
        :param xcPierSectionMaterial: XC section material for the pier.
        :param linearElastic: if True, assign a linear elastic material to
                              struts and ties (insteaa of an no-tension or
                              no-compression material). Used with debugging
                              purposes.
        '''
        pierBottomNodePos= self.pierBottomNode.getInitialPos3d
        pileBottomNodePosA= self.pileTopNodeA.getInitialPos3d
        pileBottomNodePosB= self.pileTopNodeB.getInitialPos3d
        pileBottomNodePosC= self.pileTopNodeC.getInitialPos3d
        bottomTriangle= geom.Triangle3d(pileBottomNodePosA, pileBottomNodePosB, pileBottomNodePosC)
        bottomCentroid= bottomTriangle.getCenterOfMass()
        auxLineA= geom.Segment3d(bottomCentroid, pileBottomNodePosA)
        auxLineB= geom.Segment3d(bottomCentroid, pileBottomNodePosB)
        auxLineC= geom.Segment3d(bottomCentroid, pileBottomNodePosC)
        bottomPlane= bottomTriangle.getPlane()
        kVector= bottomPlane.getNormal().normalized()
        d= bottomPlane.dist(pierBottomNodePos) # effective depth.
        # Compute the position of the pile top nodes.
        pileTopNodePosA= pileBottomNodePosA+d*kVector
        pileTopNodePosB= pileBottomNodePosB+d*kVector
        pileTopNodePosC= pileBottomNodePosC+d*kVector
        # Compute the position of the lateral intermediate nodes.
        midBottomNodePosAB= geom.Segment3d(pileBottomNodePosA, pileBottomNodePosB).getMidPoint()
        midTopNodePosAB= geom.Segment3d(pileTopNodePosA, pileTopNodePosB).getMidPoint()
        midBottomNodePosBC= geom.Segment3d(pileBottomNodePosB, pileBottomNodePosC).getMidPoint()
        midTopNodePosBC= geom.Segment3d(pileTopNodePosB, pileTopNodePosC).getMidPoint()
        midBottomNodePosCA= geom.Segment3d(pileBottomNodePosC, pileBottomNodePosA).getMidPoint()
        midTopNodePosCA= geom.Segment3d(pileTopNodePosC, pileTopNodePosA).getMidPoint()
        # Compute the positions of the pier nodes.
        radius= self.pierEffectiveDiameter/2.0
        pierBottomNodePosA= auxLineA.getPoint(radius)
        pierBottomNodePosB= auxLineB.getPoint(radius)
        pierBottomNodePosC= auxLineC.getPoint(radius)
        pierTopNodePosA= pierBottomNodePosA+d*kVector
        pierTopNodePosB= pierBottomNodePosB+d*kVector
        pierTopNodePosC= pierBottomNodePosC+d*kVector

        # Create the pile cap nodes.
        ## Nodes over the piles.
        pileBottomNodeA= self.pileTopNodeA # already exists.
        pileBottomNodeB= self.pileTopNodeB # already exists.
        pileBottomNodeC= self.pileTopNodeC # already exists.
        pileTopNodeA= modelSpace.newNodePos3d(pileTopNodePosA)
        pileTopNodeB= modelSpace.newNodePos3d(pileTopNodePosB)
        pileTopNodeC= modelSpace.newNodePos3d(pileTopNodePosC)
        ## Intermediate nodes.
        midBottomNodeAB= modelSpace.newNodePos3d(midBottomNodePosAB)
        midTopNodeAB= modelSpace.newNodePos3d(midTopNodePosAB)
        midBottomNodeBC= modelSpace.newNodePos3d(midBottomNodePosBC)
        midTopNodeBC= modelSpace.newNodePos3d(midTopNodePosBC)
        midBottomNodeCA= modelSpace.newNodePos3d(midBottomNodePosCA)
        midTopNodeCA= modelSpace.newNodePos3d(midTopNodePosCA)
        ## Nodes under the pier.
        pierBottomNodeA= modelSpace.newNodePos3d(pierBottomNodePosA)
        pierBottomNodeB= modelSpace.newNodePos3d(pierBottomNodePosB)
        pierBottomNodeC= modelSpace.newNodePos3d(pierBottomNodePosC)
        pierTopNodeA= modelSpace.newNodePos3d(pierTopNodePosA)
        pierTopNodeB= modelSpace.newNodePos3d(pierTopNodePosB)
        pierTopNodeC= modelSpace.newNodePos3d(pierTopNodePosC)
        # Define elements.
        ## Define struts.
        ### Define material.
        if(linearElastic):
            concreteNoTension= concrete.defElasticMaterial(preprocessor= modelSpace.preprocessor)
        else:
            concreteNoTension= concrete.defElasticNoTensMaterial(preprocessor= modelSpace.preprocessor, a= .001)
        modelSpace.setElementDimension(3)
        modelSpace.setDefaultMaterial(concreteNoTension)
        
        ### Radial struts.
        radialStrutsNodes= [(pierTopNodeA, pileBottomNodeA), (pierBottomNodeA, pileTopNodeA), (pierTopNodeB, pileBottomNodeB), (pierBottomNodeB, pileTopNodeB), (pierTopNodeC, pileBottomNodeC), (pierBottomNodeC, pileTopNodeC)]
        self.radialStruts= list()
        for (n1, n2) in radialStrutsNodes:
            newStrut= modelSpace.newElement("Truss", [n1.tag, n2.tag])
            newStrut.sectionArea= strutArea
            self.radialStruts.append(newStrut)

        ### Struts on the perimeter.
        pilesContourBottomNodes= [pileBottomNodeA, pileBottomNodeB, pileBottomNodeC] 
        pilesContourTopNodes= [pileTopNodeA, pileTopNodeB, pileTopNodeC]
        midContourBottomNodes= [midBottomNodeAB, midBottomNodeBC, midBottomNodeCA] 
        midContourTopNodes= [midTopNodeAB, midTopNodeBC, midTopNodeCA]
        contourBottomNodes= list()
        for pileBottomNode, midBottomNode in zip(pilesContourBottomNodes, midContourBottomNodes):
            contourBottomNodes.append(pileBottomNode)
            contourBottomNodes.append(midBottomNode)
        contourBottomNodes.append(contourBottomNodes[0]) # close "circuit".
        contourTopNodes= list()
        for pileTopNode, midTopNode in zip(pilesContourTopNodes, midContourTopNodes):
            contourTopNodes.append(pileTopNode)
            contourTopNodes.append(midTopNode)
        contourTopNodes.append(contourTopNodes[0]) # close "circuit".
        
        self.perimeterStruts= list()
        n0Bottom= contourBottomNodes[0]
        n0Top= contourTopNodes[0]
        for (n1Bottom, n1Top) in zip(contourBottomNodes[1:], contourTopNodes[1:]):
            newStrut= modelSpace.newElement("Truss", [n0Bottom.tag, n1Top.tag])
            newStrut.sectionArea= strutArea
            self.perimeterStruts.append(newStrut)
            newStrut= modelSpace.newElement("Truss", [n0Top.tag, n1Bottom.tag])
            newStrut.sectionArea= strutArea
            self.perimeterStruts.append(newStrut)
            n0Bottom= n1Bottom
            n0Top= n1Top

        ### Pier struts.
        pierContourBottomNodes= [pierBottomNodeA, pierBottomNodeB, pierBottomNodeC, pierBottomNodeA] 
        pierContourTopNodes= [pierTopNodeA, pierTopNodeB, pierTopNodeC, pierTopNodeA] 
        self.pierStruts= list()
        n0Bottom= pierContourBottomNodes[0]
        n0Top= pierContourTopNodes[0]
        for (n1Bottom, n1Top) in zip(pierContourBottomNodes[1:], pierContourTopNodes[1:]):
            newStrut= modelSpace.newElement("Truss", [n0Bottom.tag, n1Top.tag])
            newStrut.sectionArea= strutArea
            self.pierStruts.append(newStrut)
            newStrut= modelSpace.newElement("Truss", [n0Top.tag, n1Bottom.tag])
            newStrut.sectionArea= strutArea
            self.pierStruts.append(newStrut)
            n0Bottom= n1Bottom
            n0Top= n1Top
        
        ## Define ties.
        ### Define material.
        if(linearElastic):
            steelNoCompression= reinfSteel.defElasticMaterial(preprocessor= modelSpace.preprocessor)
        else:
            steelNoCompression= reinfSteel.defElasticNoCompressionMaterial(preprocessor= modelSpace.preprocessor, a= .001)
        modelSpace.setDefaultMaterial(steelNoCompression)
        modelSpace.setElementDimension(3)

        ### Define radial ties.
        radialTiesNodes= [(pierTopNodeA, pileTopNodeA), (pierBottomNodeA, pileBottomNodeA), (pierTopNodeB, pileTopNodeB), (pierBottomNodeB, pileBottomNodeB), (pierTopNodeC, pileTopNodeC), (pierBottomNodeC, pileBottomNodeC)]
        self.radialTies= list()
        for (n1, n2) in radialTiesNodes:
            newTie= modelSpace.newElement("Truss", [n1.tag, n2.tag])
            newTie.sectionArea= radialTiesArea
            self.radialTies.append(newTie)

        ### Define ties on the perimeter.
        #### Top chord.
        self.topChordTies= list()
        n0Top= contourTopNodes[0]
        for n1Top in contourTopNodes[1:]:
            newTie= modelSpace.newElement("Truss", [n0Top.tag, n1Top.tag])
            newTie.sectionArea= topChordsTiesArea
            self.topChordTies.append(newTie)
            n0Top= n1Top
        self.bottomChordTies= list()
        #### Bottom chord.
        n0Bottom= contourBottomNodes[0]
        for n1Bottom in contourBottomNodes[1:]:
            newTie= modelSpace.newElement("Truss", [n0Bottom.tag, n1Bottom.tag])
            newTie.sectionArea= bottomChordsTiesArea
            self.bottomChordTies.append(newTie)
            n0Bottom= n1Bottom
        #### Vertical ties over each pile.
        for (nBottom, nTop) in zip(pilesContourBottomNodes, pilesContourTopNodes):
            newTie= modelSpace.newElement("Truss", [nBottom.tag, nTop.tag])
            newTie.sectionArea= pileTiesArea
            self.bottomChordTies.append(newTie)
        #### Shear ties between piles.
        for (nBottom, nTop) in zip(midContourBottomNodes, midContourTopNodes):
            newTie= modelSpace.newElement("Truss", [nBottom.tag, nTop.tag])
            newTie.sectionArea= shearTiesArea
            self.bottomChordTies.append(newTie)

        ### Define pier ties.
        #### Top chord.
        self.pierTopChordTies= list()
        n0Top= pierContourTopNodes[0]
        for n1Top in pierContourTopNodes[1:]:
            newTie= modelSpace.newElement("Truss", [n0Top.tag, n1Top.tag])
            newTie.sectionArea= topChordsTiesArea
            self.pierTopChordTies.append(newTie)
            n0Top= n1Top
        #### Bottom chord.
        self.pierBottomChordTies= list()
        n0Bottom= pierContourBottomNodes[0]
        for n1Bottom in pierContourBottomNodes[1:]:
            newTie= modelSpace.newElement("Truss", [n0Bottom.tag, n1Bottom.tag])
            newTie.sectionArea= bottomChordsTiesArea
            self.pierBottomChordTies.append(newTie)
            n0Bottom= n1Bottom
        
        ### Define dummy springs (to fix rotational DOFs only).
        nodesToConstrain= contourTopNodes+midContourBottomNodes+pierContourBottomNodes
        springsAndNodes= strut_and_tie_utils.define_dummy_springs(modelSpace, nodesToConstrain)
        
        ### Connect the pier with the pilecap using the pier section
        ### as "rigid beam".
        modelSpace.setDefaultMaterial(xcPierSectionMaterial)
        n0Tag= self.pierBottomNode.tag
        n1Tag= pierContourTopNodes[1].tag
        n2Tag= pierContourTopNodes[2].tag
        n3Tag= pierContourTopNodes[3].tag
        crdTransfName= str(uuid.uuid4().hex)
        xzVector= xc.Vector([kVector.x, kVector.y, kVector.z])
        crdTransf= modelSpace.newLinearCrdTransf(crdTransfName, xzVector= xzVector)
        modelSpace.setDefaultCoordTransf(crdTransf)
        modelSpace.newElement('ElasticBeam3d', [n0Tag, n1Tag])
        modelSpace.newElement('ElasticBeam3d', [n0Tag, n2Tag])
        modelSpace.newElement('ElasticBeam3d', [n0Tag, n3Tag])

    

