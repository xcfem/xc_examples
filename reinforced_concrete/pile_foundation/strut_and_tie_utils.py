# -*- coding: utf-8 -*-
''' Utilities for the generation of strut-and-tie models.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis Claudio Pérez Tato (LCPT)"
__copyright__= "Copyright 2025, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import xc
from materials import typical_materials

dummy_spring_material= None
dummy_spring_material_name= 'strut-and-tie_dummy_spring_material'
dummy_spring_stiffness= 1e6

def create_dummy_spring(modelSpace, node):
    ''' Put a spring to constrain the rotation of the given node. The nodes that
        are connected only to struts and ties can rotate freely, and that makes
        the model stiffness matrix singular. This function is used to avoid
        that.

    :param modelSpace: PredefinedSpace object used to create the FE model.
    :param node: node whose rotations need to be constrained.
    '''
    global dummy_spring_material
    if(dummy_spring_material is None):
        preprocessor= modelSpace.preprocessor
        dummy_spring_material= typical_materials.defElasticMaterial(preprocessor, "dummy_spring_stiffness", dummy_spring_stiffness)
    nDOFs= node.getNumberDOF
    dim= node.dim
    if((nDOFs==3) and (dim==2)): # 2D structural.
        dimElem= 3
        constrainedDOFs= [2]
    elif((nDOFS==6) and (dim==3)): # 3D structural.
        dimElem= 6
        constrainedDOFs= [3, 4, 5]
    else:
        className= type(self).__name__
        methodName= sys._getframe(0).f_code.co_name
        errorMessage= className+'.'+methodName+'; unknown rotational DOFs.'
        lmsg.error(errMsg)
    newNode= modelSpace.duplicateNode(node) # new node.
    # Create the spring.
    modelSpace.setDefaultMaterial(dummy_spring_material)
    modelSpace.setElementDimension(dimElem)
    zl= modelSpace.newElement("ZeroLength",[newNode.tag, node.tag])
    zl.clearMaterials()
    for dof in constrainedDOFs:
        print('node tag: ', node.tag, 'dof: ', dof, ' stiffness: ', dummy_spring_material.getTangent()/1e6)
        zl.setMaterial(dof, dummy_spring_material.name)
    # Boundary conditions: fix the newly created node.
    numDOFs= newNode.getNumberDOF
    newNodeTag= newNode.tag
    for dof in range(0,numDOFs):
        print('node tag: ', newNodeTag, ' DOF: ', dof)
        spc= modelSpace.newSPConstraint(newNodeTag, dof, 0.0)
        if(__debug__):
            if(not spc):
                AssertionError('Can\'t create the constraint.')
    return zl, newNode

def define_dummy_springs(modelSpace, nodes):
    ''' Put a spring to constrain the rotation of the given nodes. The nodes
        that are connected only to struts and ties can rotate freely, and that
        makes the model stiffness matrix singular. This function is used to
        avoid that.

    :param modelSpace: PredefinedSpace object used to create the FE model.
    :param node: node whose rotations need to be constrained.
    '''
    # Get the current default materials.
    previousDefaultMaterials= modelSpace.getDefaultMaterials()
    retval= list()
    for node in nodes:
        zl, newNode= create_dummy_spring(modelSpace, node)
    retval.append((zl, newNode))
    # Revert the default materials.
    modelSpace.setDefaultMaterials(previousDefaultMaterials)
    return retval

    
