# -*- coding: utf-8 -*-
from __future__ import division 

import math
import xc_base
import geom
import xc
from materials.sections.structural_shapes import aisc_metric_shapes as lb
from materials.astm_aisc import ASTM_materials

# Generic functions
def cross(xcV1,xcV2):
    '''cross product of two xc vectors of 3-D
    '''
    v1=geom.Vector3d(xcV1[0],xcV1[1],xcV1[2])
    v2=geom.Vector3d(xcV2[0],xcV2[1],xcV2[2])
    vcross=v1.cross(v2)
    xcVcross=xc.Vector([vcross.x,vcross.y,vcross.z])
    return xcVcross
            
def getSuitableXZVector(iNode, jNode):
    ''' Return a vector that can be used to define
        a coordinate transformation for an element
        between the node arguments.

    :param iNode: first node.
    :param jNode: second node.
    '''
    p1= iNode.getInitialPos3d
    p2= jNode.getInitialPos3d
    sg= geom.Line3d(p1,p2)
    v3d= sg.getKVector
    return xc.Vector([v3d.x, v3d.y, v3d.z])

def setBearingBetweenNodes(prep,iNodA,iNodB,bearingMaterialNames,orientation= None):
    '''Modelize a bearing between the nodes

     :param iNodA: (int) first node identifier (tag).
     :param iNodB: (int) second node identifier (tag).
     :param bearingMaterialNames: (list) material names for the zero 
        length element [mat1,mat2,mat3,mat4,mat5,mat6], where:
        mat1,mat2,mat3 correspond to translations along local x,y,z 
        axes, respectively,
        mat3,mat4,mat5 correspond to rotation about local x,y,z 
        axes, respectively.
     :param orientation: (list) of two vectors [x,yp] used to orient 
        the zero length element, where: 
        x: are the vector components in global coordinates defining 
           local x-axis (optional)
        yp: vector components in global coordinates defining a  vector
             that lies in the local x-y plane of the element(optional).
      If the optional orientation vector are not specified, the local
      element axes coincide with the global axes. Otherwise, the local
      z-axis is defined by the cross product between the vectors x 
      and yp specified in the command line.
      :return: newly created zero length element that represents the bearing.

    '''
    # Element definition
    elems= prep.getElementHandler
    elems.dimElem= prep.getNodeHandler.dimSpace # space dimension.
    elems.defaultMaterial= next((item for item in bearingMaterialNames if item is not None), 'All are Nones')
    zl= elems.newElement("ZeroLength",xc.ID([iNodA,iNodB]))
    zl.clearMaterials()
    if(orientation): #Orient element.
        zl.setupVectors(orientation[0],orientation[1])
    numMats= len(bearingMaterialNames)
    for i in range(0,numMats):
        material= bearingMaterialNames[i]
        if(material!=None):
            zl.setMaterial(i,material)
    return zl

def print_shape_dim(shape,ang=0):
    ''' print dimensions of the steel shape
    :param angle: angle of the cutting plane with respect to perpendicular
                  to member longitudinal axis (defaults to 0).
    '''
    cosAng=math.cos(math.radians(ang))
    print('Shape: ', lb.getMetricLabel(shape.name))
    print('b= ', round(shape.b()*1e3,1),' mm, h= ',  round(shape.h()/cosAng*1e3,1),' mm')
    print('tw= ',round(shape.tw()*1e3,1),' mm, tf= ',round(shape.tf()/cosAng*1e3,1),' mm \n')

def print_plate_shear(descr,h,t,steel,Vd,profile=None):
    '''
    :param descr: plate description
    :param h: height of the plate
    :param t: thickness of the plate
    :param steel: steel of the plate
    :param Vd: shear
    :param profile: beam profile (defautls to None)
    '''
    # Print back-plate dimensions and capacity factors
    print (descr+' heigth= ', round(h*1e3,1), ' mm, thickness= ',round(t*1e3,1), ' mm')
    if profile:
        shear_strength_beam=profile.getNominalShearStrengthWithoutTensionFieldAction()
        # thickness of the plate to have the same strength:
        strict_thick=shear_strength_beam/(0.6*steel.fy*h)
        print(descr+ ' thickness to equal profile shear strength: ', round(strict_thick*1e3,1), ' mm')

    # strength shear yielding
    Rn=0.6*steel.fy*h*t
    fi=1
    print(descr+ ' strength for shear yielding: fiRn= ', round(fi*Rn*1e-3,1), ' kN,  CF= ', round( Vd/(fi*Rn),2))

    # strength shear rupture
    Rn=0.6*steel.fu*h*t
    fi=0.75
    print(descr+ ' strength for shear rupture: fiRn= ', round(fi*Rn*1e-3,1), ' kN,  CF= ', round( Vd/(fi*Rn),2))
   

def print_max_min_weld_size(profile,plateThck):
    '''Return the maximum and minimum weld sizes between the web and the 
    flanges of the profile and a plate of thickness plateThck
    '''
    print(lb.getMetricLabel(profile.name),' to plate of thickness ', round(plateThck*1e3,1), ' mm')
    z_min=round(ASTM_materials.getFilletWeldMinimumLegSheets(profile.tw(),plateThck)*1e3,1)
    z_max=round(ASTM_materials.getFilletWeldMaximumLegSheets(profile.tw(),plateThck)*1e3,1)
    print('Weld plate to web: z_min= ', z_min,' mm, z_max= ', z_max,' mm')
    z_min=round(ASTM_materials.getFilletWeldMinimumLegSheets(profile.tf(),plateThck)*1e3,1)
    z_max=round(ASTM_materials.getFilletWeldMaximumLegSheets(profile.tf(),plateThck)*1e3,1)
    print('Weld plate to flange: z_min= ', z_min,' mm, z_max= ', z_max,' mm \n')
    
def print_bolt_dim(boltDiam,boltSteel):
    '''Return bolt dimensions and minimum distances between centers and to
    the edge.
    '''
    b=ASTM_materials.BoltFastener(boltDiam,boltSteel)
    print('* Bolt dimensions *')
    print('bolt diameter = ', round(b.diameter*1e3,1), ' mm')
    print('hole diameter = ', round(b.getNominalHoleDiameter()*1e3,1), ' mm')
    print('minimum distance between b centers = ', round(b.getMinDistanceBetweenCenters()*1e3,1), ' mm')
    print('minimum edge distance = ', round(b.getMinimumEdgeDistance()*1e3,1), ' mm')
    

    
