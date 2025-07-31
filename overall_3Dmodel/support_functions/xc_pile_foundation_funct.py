# -*- coding: utf-8 -*-
import math
import xc
import geom
from materials import typical_materials
from model.mesh import finit_el_model as fem
from geotechnics.foundations import guia_cimentaciones_oc as guia

# Deep foundation model. Strut and tie model of the pilecap and pile model according to «guía de cimentaciones»
def gen_fict_beam(modelSpace,nodCol,nodPile,fictBmLenght,fictBmSectMat,fictBeamSet):
    ''' Generate an horizontal fictitious beam contained in the vertical plane
    passing through the pier bottom node and a pile top node. Return the two
    nodes at the extremities of the beam (fbNode1 is the furthest from the
    pile and fbNode2 the closest to the pile). These nodes will be used to
    define struts between a fictitious beam and a pile.
    The elements created are added to fictBeamSet.

    :param modelSpace: model space
    :param nodCol: bottom node of the column
    :param nodPile: top node of the pile
    :param fictBmLenght: length of the fictitious beam created
    :param fictBmSectMat: section-material to assign to the fictitious beam (e.g. matFbeams=
                    typical_materials.defElasticSectionFromMechProp3d(prep, "matFbeams",sectionProperties)
    :param fictBeamSet:set to which add the new fictitious beam created
    '''
    nodes=modelSpace.getNodeHandler()
    elems=modelSpace.getElementHandler()
    (xNodCol,yNodCol,zNodCol)=nodCol.get3dCoo
    (xNodPile,yNodPile,zNodPile)=nodPile.get3dCoo
    vFbeam=geom.Vector2d(xNodPile-xNodCol,yNodPile-yNodCol)
    vFbeam.normalize(); vFbeam=fictBmLenght/2*vFbeam
    fbNode1=nodes.newNodeXYZ(xNodCol+vFbeam[0],yNodCol+vFbeam[1],zNodCol)
    fbNode2=nodes.newNodeXYZ(xNodCol-vFbeam[0],yNodCol-vFbeam[1],zNodCol)
    # generation of fictitius beam
    elems.defaultMaterial=fictBmSectMat.name
    lin= modelSpace.newLinearCrdTransf("linZ",xc.Vector([0,0,1]))
    elems.defaultTransformation=lin.name
    fbeam1=elems.newElement("ElasticBeam3d",xc.ID([fbNode1.tag,nodCol.tag])); fictBeamSet.elements.append(fbeam1)
    fbeam2=elems.newElement("ElasticBeam3d",xc.ID([nodCol.tag,fbNode2.tag])); fictBeamSet.elements.append(fbeam2)
    return fbNode1,fbNode2


def gen_struts(modelSpace,pairNod,nodPile,strutArea, strutMat,strutSet,):
    ''' Generate two struts elements between the top node of the pile
    and each one of the pair of nodes given asa parameter (nodes then
    belong to the fictious beams previously created in cantilever
        bottom node of the column (and rigidly joint to it). 
    The generated struts are added to strutSet.

    :param modelSpace: model space
    :param pairNod: list of two nodes of fictious beams
    :param nodPile: top node of the pile
    :param strutArea: cross-section area of the struts
    :param strutMat: strut material (e.g. matStrut=
           typical_materials.defElasticMaterial(prep,'matStrut',concrete.Ecm())
    :param strutSet: set to which add the new struts created
    :param fictBmLenght: length of the fictitious beam created
    :param fictBmSectMat: section-material to assign to the fictitious beam (e.g. matFbeams=
                    typical_materials.defElasticSectionFromMechProp3d(prep, "matFbeams",sectionProperties)
    :param fictBeamSet:set to which add the new fictitious beam created
    :param genFictBeam: True to create the fictitious beam, False if it exists
    '''
    # generation of strut elements
    elems=modelSpace.getElementHandler()
    elems.defaultMaterial=strutMat.name
    fbNode1=pairNod[0]; fbNode2=pairNod[1]
    strut1=elems.newElement("Truss",xc.ID([fbNode1.tag,nodPile.tag])) ;strut1.sectionArea=strutArea ; strutSet.elements.append(strut1)
    strut2=elems.newElement("Truss",xc.ID([fbNode2.tag,nodPile.tag])) ; strut2.sectionArea=strutArea ; strutSet.elements.append(strut2)

    
def gen_tie(modelSpace,nodPile1,nodPile2,tieArea,tieMat,tieSet):
    ''' Generate a tie element between top nodes of pile1 and pile2
    and append it to tieSet

    :param modelSpace: model space
    :param nodPile1, nodPile2 : top node of two linked piles
    :param tieArea: cross-section area of the ties
    :param tieMat: tie material (e.g. matTie=
           typical_materials.defElasticMaterial(prep,'matTie',concrete.Ecm())
    :param tieSet: set to which add the new ties created

    '''
    elems=modelSpace.getElementHandler()
    elems.defaultMaterial=tieMat.name
    tie=elems.newElement("Truss",xc.ID([nodPile1.tag,nodPile2.tag])) ;tie.sectionArea=tieArea ; tieSet.elements.append(tie)
    return
    
def gen_pile(modelSpace,topNodPile,pileDiam,pileLenght,pileMat,eSize,pileType,bearingCapPile,groundLevel,soils,pileSet,alphaK=[1,1,1]):
    '''Generate a pile, append its elements to pileSet and return its bottom
    node and the pile boundary conditions (springs).

    :param modelSpace: model space
    :param topNodPile: top node of the pile
    :param pileDiam: diameter of the pile.
    :param pileLenght: length of the pile.
    :param pileMat: pile section-material.
    :param eSize: size of the elements.
    :param pileType: type of pile 'endBearing' or 'friction'.
    :param bearingCapPile: total bearing capacity of the pile
    :param groundLevel: global Z coordinate of the ground level 
    :param soils: list of soil definition  [(zBottom,type, prop), ...]
                  where 'zBottom' is the global 
                  Z coordinate of the bottom level of the soil,
                  type is the type o soil ("sand" or "clay")
                  prop is the soil property : compactness [Pa/m]
                  for sandy soils and undrained soil shear
                  strength for clay soils.
    :param pileSet: set to which add the pile elements
    :param alphaK: coefficients [alphaKh_x,alphaKh_y,alphaKh_z] to take
                   into account the pile group
                   effect (defaults to [1,1,1])
    '''
    prep=modelSpace.preprocessor
    nodes=modelSpace.getNodeHandler()
    elems=modelSpace.getElementHandler()
    elems.defaultMaterial=pileMat.name
    lin= modelSpace.newLinearCrdTransf("linX",xc.Vector([1,0,0]))
    elems.defaultTransformation=lin.name
    nElems=int(pileLenght/eSize)
    zStep=pileLenght/nElems
    nodSup=topNodPile
    x0,y0,z0=nodSup.getCoo[0],nodSup.getCoo[1],nodSup.getCoo[2]
    auxSet=prep.getSets.defSet('auxSet')
    for i in range(nElems):
        z=z0-(i+1)*zStep
        n=nodes.newNodeXYZ(x0,y0,z)
        e=elems.newElement('ElasticBeam3d',xc.ID([n.tag,nodSup.tag]))
        auxSet.elements.append(e)
        pileSet.elements.append(e)
        nodSup=n
    nBottPile=n
    auxSet.fillDownwards()
    modelSpace.fixNode('FF0_000',nBottPile.tag)
    soilLayers= guia.SoilLayers(soilProfile= soils, groundLevel= groundLevel)
    pileBC=guia.PileFoundation(pileSet=auxSet,pileDiam=pileDiam,E=pileMat.E,pileType=pileType,pileBearingCapacity=bearingCapPile, soilLayers=soilLayers)
    pileBC.generateSpringsPile(alphaK[0],alphaK[1],alphaK[2])
    prep.getSets.removeSet('auxSet')
    return nBottPile, pileBC
    
                            
