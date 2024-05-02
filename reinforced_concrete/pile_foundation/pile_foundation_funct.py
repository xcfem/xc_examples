# -*- coding: utf-8 -*-
import math
import xc
import geom
from materials import typical_materials
from model.mesh import finit_el_model as fem
from geotechnics.foundations import guia_cimentaciones_oc as guia

def gen_fict_colum_section_nod(nodHdl,nodCol,LxFictCol,LyFictCol):
    '''Return a list of nodes for the fictitious column (section contained in the real cross-section of the column)178

    The nodes are arranged clockwise [(xmin,ymn),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
    
    :param nodHdl: nodel handler
    :param nodCol: node of the column
    :param LxFictCol: width of the fictitious column in X direction
    :param LyFictCol: width of the fictitious column in Y direction
    '''
    (xNodCol,yNodCol,zNodCol)=nodCol.get3dCoo
    nodFictC1= nodHdl.newNodeXYZ(xNodCol-LxFictCol/2.,yNodCol-LyFictCol/2.,zNodCol)
    nodFictC2= nodHdl.newNodeXYZ(xNodCol+LxFictCol/2.,yNodCol-LyFictCol/2.,zNodCol)
    nodFictC3= nodHdl.newNodeXYZ(xNodCol+LxFictCol/2.,yNodCol+LyFictCol/2.,zNodCol)
    nodFictC4= nodHdl.newNodeXYZ(xNodCol-LxFictCol/2.,yNodCol+LyFictCol/2.,zNodCol)
    return [nodFictC1,nodFictC2,nodFictC3,nodFictC4]
   
def gen_fict_colum_section_elems(modelSpace,nodCol,nodFictLst,concrete,areaFictCol,fbeamSet):
    '''Generate the elements of the fictitious column (section contained in the real cross-section of the column)
    and appends them to set fbeamSet

    :param modelSpace: model space
    :param nodCol: node of the column
    :param nodFictLst: list of nodes for the fictitious column arranged clockwise [(xmin,ymn),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
    :param concrete: concrete
    :param areaFictCol: cross-section area of the fictitious beams in the base of the column
    :param fbeamSet: set of the fictitious column beam elements
    '''
    elemHdl=modelSpace.getElementHandler() ; prep=modelSpace.preprocessor
    sectionProperties= xc.CrossSectionProperties3d()
    b=math.sqrt(areaFictCol); h=b ; I=1/12*b*h**3
    sectionProperties.A= areaFictCol; sectionProperties.E= concrete.Ecm();
    sectionProperties.G= concrete.Ecm()/(2*(1+concrete.nuc))
    sectionProperties.Iz=I; sectionProperties.Iy=I; sectionProperties.J=1/3*b**4*0.40147
    matFbeams=typical_materials.defElasticSectionFromMechProp3d(prep, "matFbeams",sectionProperties)
    elemHdl.defaultMaterial='matFbeams'
    lin= modelSpace.newLinearCrdTransf("lin",xc.Vector([0,0,1]))
    elemHdl.defaultTransformation=lin.name
    (nodFictC1,nodFictC2,nodFictC3,nodFictC4)=nodFictLst
    fbeam01=elemHdl.newElement("ElasticBeam3d",xc.ID([nodFictC1.tag,nodCol.tag]))
    fbeam02=elemHdl.newElement("ElasticBeam3d",xc.ID([nodCol.tag,nodFictC2.tag]))
    fbeam03=elemHdl.newElement("ElasticBeam3d",xc.ID([nodCol.tag,nodFictC3.tag]))
    fbeam04=elemHdl.newElement("ElasticBeam3d",xc.ID([nodFictC4.tag,nodCol.tag]))
    for e in [fbeam01,fbeam02,fbeam03,fbeam04]:
        fbeamSet.elements.append(e)

def gen_strut_elems(elemHdl,nodFictLst,nodPilLst,concrete,areaStrut,strutSet):
    '''Generate the strut elements and append them to set strutSet

    :param elemHdl: element handler
    :param nodCol: node of the column
    :param nodFictLst: list of nodes for the fictitious column arranged clockwise [(xmin,ymn),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
    :param nodPilLst: list of top nodes for the piles arranged clockwise [(xmin,ymn),(xmin,ymax),(xmax,ymax),(xmax,ymin)]
    :param concrete: concrete
    :param areaStrut: cross-section area of the strut
    :param fbeamSet: set of the struts
    '''
    prep=elemHdl.getPreprocessor
    matStrut=typical_materials.defElasticMaterial(prep,'matStrut',concrete.Ecm())
    matStrut.E=concrete.Ecm()
    elemHdl.defaultMaterial=matStrut.name
    (nodFictC1,nodFictC2,nodFictC3,nodFictC4)=nodFictLst
    (nodPil1,nodPil2,nodPil3,nodPil4)=nodPilLst
    str1a= elemHdl.newElement("Truss",xc.ID([nodFictC1.tag,nodPil1.tag]))
    str1b= elemHdl.newElement("Truss",xc.ID([nodFictC3.tag,nodPil1.tag]))
    str2a= elemHdl.newElement("Truss",xc.ID([nodFictC2.tag,nodPil2.tag]))
    str2b= elemHdl.newElement("Truss",xc.ID([nodFictC4.tag,nodPil2.tag]))
    str3a= elemHdl.newElement("Truss",xc.ID([nodFictC3.tag,nodPil3.tag]))
    str3b= elemHdl.newElement("Truss",xc.ID([nodFictC1.tag,nodPil3.tag]))
    str4a= elemHdl.newElement("Truss",xc.ID([nodFictC4.tag,nodPil4.tag]))
    str4b= elemHdl.newElement("Truss",xc.ID([nodFictC2.tag,nodPil4.tag]))
    for e in [str1a,str1b,str2a,str2b,str3a,str3b,str4a,str4b]:
        e.sectionArea=areaStrut
        strutSet.getElements.append(e)
    

def gen_pile_cap_1column_4piles(modelSpace,concrete,steel,nodCol,LxFictCol,LyFictCol,areaFictCol,distXpile,distYpile,Hpilecap,areaStrut,areaTie,nameSetStruts,nameSetTies,nameSetFbeams):
    '''Generate pile cap for one column with a pile foundation of 4 piles. Return the two sets of elemHdl generated (struts and ties)  and the nodes where piles start (topNodPiles)
    The fictitious column is a section contained in the real cross-section of the column 

    :param modelSpace: model space
    :param nodCol: node of the column
    :param LxFictCol: width of the fictitious column in X direction
    :param LyFictCol: width of the fictitious column in Y direction
    :param areaFictCol: cross-section area of the fictitious beams in the base of the column
    :param distXpile: distance between piles in X direction
    :param distYpile: distance between piles in Y direction
    :param Hpilecap: pile-cap height
    :param areaStrut: cross-section area of the struts
    :param areaTie: cross-section area of the ties
    :param nameSetStruts: name of the set of struts
    :param nameSetTies: name of the set of ties
    :param nameSetFbeams: name of the set of fictitious beams
    '''
    
    (xNodCol,yNodCol,zNodCol)=(nodCol.get3dCoo[0],nodCol.get3dCoo[1],nodCol.get3dCoo[2])
    prep=modelSpace.preprocessor
    nodes=modelSpace.getNodeHandler()
    lines=modelSpace.getLineHandler()
    elements=modelSpace.getElementHandler()
    struts=prep.getSets.defSet(nameSetStruts)
    ties=prep.getSets.defSet(nameSetTies)
    fbeams=prep.getSets.defSet(nameSetFbeams)
    dimElem=nodes.dimSpace
    elements.dimElem=dimElem
    
    # nodes in the fictitious column section
    nodFictLst=gen_fict_colum_section_nod(nodes,nodCol,LxFictCol,LyFictCol)
    # Fictitious beam elements
    gen_fict_colum_section_elems(modelSpace,nodCol,nodFictLst,concrete,areaFictCol,fbeams)
    # nodes in the top of the piles
    nodPil1= nodes.newNodeXYZ(xNodCol-distXpile/2.,yNodCol-distYpile/2.,zNodCol-Hpilecap)
    nodPil2= nodes.newNodeXYZ(xNodCol+distXpile/2.,yNodCol-distYpile/2.,zNodCol-Hpilecap)
    nodPil3= nodes.newNodeXYZ(xNodCol+distXpile/2.,yNodCol+distYpile/2.,zNodCol-Hpilecap)
    nodPil4= nodes.newNodeXYZ(xNodCol-distXpile/2.,yNodCol+distYpile/2.,zNodCol-Hpilecap)
    nodPilLst=[nodPil1,nodPil2,nodPil3,nodPil4]
    #Strut Elements
    gen_strut_elems(elements,nodFictLst,nodPilLst,concrete,areaStrut,struts)
    #Tie elements
    matTie=typical_materials.defElasticMaterial(prep,'matTie',steel.Es)
    matTie.E=steel.Es
    elements.defaultMaterial=matTie.name
    tie1= elements.newElement("Truss",xc.ID([nodPil1.tag,nodPil2.tag]))
    tie2= elements.newElement("Truss",xc.ID([nodPil2.tag,nodPil3.tag]))
    tie3= elements.newElement("Truss",xc.ID([nodPil3.tag,nodPil4.tag]))
    tie4= elements.newElement("Truss",xc.ID([nodPil4.tag,nodPil1.tag]))
    for e in [tie1,tie2,tie3,tie4]:
        e.sectionArea=areaTie
        ties.getElements.append(e)
    # Constraints
    topNodPiles=[nodPil1,nodPil2,nodPil3,nodPil4]
    
    struts.fillDownwards()
    ties.fillDownwards()
    return struts,ties,topNodPiles


def gen_pile_cap_Ncolumns_Nplus1x2_piles(modelSpace,concrete,steel,nodCols,LxFictCol,LyFictCol,areaFictCol,distXpile,distYpile,Hpilecap,areaStrut,areaTieX,areaTieY,nameSetStruts,nameSetTiesX,nameSetTiesY,nameSetFbeams):
    '''Generate pile cap for N columns with a pile foundation of N+1 (X direction) by  2 (Y direction) piles. Return the two sets of elements generated (struts and ties)  and the nodes where piles start (topNodPiles)

    :param modelSpace: model space
    :param nodCols: [nodeCol1,nodeCol2, ..., nodeColN] nodes of columns 1, 2, .., N in order of
                    increasing coordinate X.
    :param LxFictCol: width of the fictitious column in X direction
    :param LyFictCol: width of the fictitious column in Y direction
    :param areaFictColBeams: cross-section area of the fictitious beams in the base of the column
    :param distXpile: distance between piles in X direction
    :param distYpile: distance between piles in Y direction
    :param Hpilecap: pile-cap height
    :param areaStrut: cross-section area of the struts
    :param areaTieX: cross-section area of the ties in X direction
    :param areaTieY: cross-section area of the ties in Y direction
    :param nameSetStruts: name of the set of struts
    :param nameSetTiesX: name of the set of ties in X direction
    :param nameSetTiesY: name of the set of ties in Y direction
    :param nameSetFbeams: name of the set of fictitious beams
    '''
    prep=modelSpace.preprocessor
    nodes=modelSpace.getNodeHandler()
    lines=modelSpace.getLineHandler()
    elements=modelSpace.getElementHandler()
    struts=prep.getSets.defSet(nameSetStruts)
    tiesX=prep.getSets.defSet(nameSetTiesX)
    tiesY=prep.getSets.defSet(nameSetTiesY)
    fbeams=prep.getSets.defSet(nameSetFbeams)
    dimElem=nodes.dimSpace
    elements.dimElem=dimElem
    nodCol1=nodCols[0]
    nodCol2=nodCols[-1]
    (xCent,yCent,zCent)=((nodCol1.get3dCoo[0]+nodCol2.get3dCoo[0])/2.,
                         (nodCol1.get3dCoo[1]+nodCol2.get3dCoo[1])/2.,
                         nodCol1.get3dCoo[2])
    nCols=len(nodCols)
    # nodes in the fictitious column section
    nodFict=list()
    for n in nodCols:
        nodCol=n
        nodFict.append(gen_fict_colum_section_nod(nodes,nodCol,LxFictCol,LyFictCol))
    # Fictitious beam elements
    for i in range(nCols):
        nodCol=nodCols[i]
        nodFictLst=nodFict[i]
        gen_fict_colum_section_elems(modelSpace,nodCol,nodFictLst,concrete,areaFictCol,fbeams)
    # nodes in the top of the piles
    nodTopPiles=list()
    nRowsPil=len(nodCols)+1 #number of rows of piles in X direction 
    xPilMin=xCent-(distXpile*(nRowsPil-1))/2
    yPilMin=yCent-distXpile/2
    yPilMax=yCent+distXpile/2
    zPil=zCent-Hpilecap
    for i in range(nRowsPil):
        xPil=xPilMin+i*distXpile
        nodTopPiles.append([nodes.newNodeXYZ(xPil,yPilMin,zPil),
                            nodes.newNodeXYZ(xPil,yPilMax,zPil)])
    #strut elements
    matStrut=typical_materials.defElasticMaterial(prep,'matStrut',concrete.Ecm())
    matStrut.E=concrete.Ecm()
    elements.defaultMaterial=matStrut.name
    for i in range(nCols):
        nodFictLst=nodFict[i]
        nodPilLst=nodTopPiles[i]+[nodTopPiles[i+1][-1],nodTopPiles[i+1][0]]
        gen_strut_elems(elements,nodFictLst,nodPilLst,concrete,areaStrut,struts)
    #Tie elements
    matTie=typical_materials.defElasticMaterial(prep,'matTie',steel.Es)
    matTie.E=steel.Es
    elements.defaultMaterial=matTie.name
    # Ties in Y direction
    for pairTopNod in nodTopPiles:
        (n1,n2)=pairTopNod
        e=elements.newElement("Truss",xc.ID([n1.tag,n2.tag]))
        e.sectionArea=areaTieY
        tiesY.elements.append(e)
    # Ties in X direction
    for i in range(nCols):
        (n1,n2)=nodTopPiles[i]
        (n3,n4)=nodTopPiles[i+1]
        tieYmin=elements.newElement("Truss",xc.ID([n1.tag,n3.tag]))
        tieYmax=elements.newElement("Truss",xc.ID([n2.tag,n4.tag]))
        tieYmin.sectionArea=areaTieX; tieYmax.sectionArea=areaTieX
        tiesX.elements.append(tieYmin); tiesX.elements.append(tieYmax)
    struts.fillDownwards()
    tiesX.fillDownwards()
    tiesY.fillDownwards()
    topNodPiles=[item for sublist in nodTopPiles for item in sublist] #flatten list
    return struts,tiesX,tiesY,topNodPiles

def gen_piles(modelSpace,topNodPiles,pileDiam,pileLenght,pileMat,eSize,pileType,bearingCapPile,soils,nameSetPiles,alphaK=[1,1,1]):
    '''Generate piles that start in a pile-cap. Return the set of piles created.

    :param preprocessor: preprocessor
    :param topNodPiles: nodes of the pile-cap where piles start.
    :param pileDiam: diameter of the pile.
    :param pileLenght: length of each pile.
    :param pileMat: pile section-material.
    :param eSize: size of the elements.
    :param pileType: type of pile 'endBearing' or 'friction'.
    :param bearingCapPile: total bearing capacity of the pile
    :param soils: list of soil definition  [(zBottom,type, prop), ...]  where 'zBottom' is the global 
                  Z coordinate of the bottom level of the soil, type is the type o soil ("sand" or "clay")
                  prop is the soil property : compactness [Pa/m] for sandy soils and undrained soil shear
                  strength for clay soils.
    :param nameSetPiles: name of the set of piles created.
    :param alphaK: coefficients [alphaKh_x,alphaKh_y,alphaKh_z] to take into account the pile group
                    effect (defaults to [1,1,1])
    '''
    prep=modelSpace.preprocessor
    piles=prep.getSets.defSet(nameSetPiles)
    nodBasePilLst=list()
    for n in topNodPiles:
        auxPileSet=prep.getSets.defSet('auxPileSet')
        x,y,z=n.getCoo[0],n.getCoo[1],n.getCoo[2]
        p1=prep.getMultiBlockTopology.getPoints.newPoint(geom.Pos3d(x,y,z))
        p0=prep.getMultiBlockTopology.getPoints.newPoint(geom.Pos3d(x,y,z-pileLenght))
        l=prep.getMultiBlockTopology.getLines.newLine(p0.tag,p1.tag)
        auxPileSet.getLines.append(l)
        auxPileSet.fillDownwards()
        pile_mesh=fem.LinSetToMesh(linSet=auxPileSet,matSect=pileMat,elemSize=eSize,vDirLAxZ=xc.Vector([0,1,0]),elemType='ElasticBeam3d',dimElemSpace=3,coordTransfType='linear')
        fem.multi_mesh(preprocessor=prep,lstMeshSets=[pile_mesh])
        soilLayers= guia.SoilLayers(soilProfile= soils, groundLevel= z)
        pileBC=guia.PileFoundation(pileSet=auxPileSet,pileDiam=pileDiam,E=pileMat.E,pileType=pileType,pileBearingCapacity=bearingCapPile, soilLayers=soilLayers)
        pileBC.generateSpringsPile(alphaK[0],alphaK[1],alphaK[2])
        springs=pileBC.springs
        n1=p1.getNode()
        n0=p0.getNode()
        nodBasePilLst.append(n0)
        modelSpace.fixNode('FF0_000',n0.tag)
        modelSpace.setRigidBeamBetweenNodes(n.tag,n1.tag)
        piles+=auxPileSet
        prep.getSets.removeSet('auxPileSet')
        piles.fillDownwards()
    return piles,nodBasePilLst
