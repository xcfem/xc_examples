# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from import_export import freecad_reader
from import_export import neutral_mesh_description as nmd
import xc_base
import geom
import xc
from model import predefined_spaces
from postprocess import output_handler

def getRelativeCoo(pt):
    return [pt[0]/1000.0,pt[1]/1000.0,pt[2]/1000.0]

groupsToImport= ['.*']

baseName= './freecad_import_test'
#baseName= './tablero'
freeCADFileName= baseName+'.FCStd'
freeCADImport= freecad_reader.FreeCADImport(freeCADFileName, groupsToImport, getRelativeCoo, threshold= 0.001)

#Block topology
blocks= freeCADImport.exportBlockTopology('test')

ieData= nmd.XCImportExportData()
ieData.outputFileName= baseName+'_blocks'
ieData.problemName= 'FEcase'
ieData.blockData= blocks

ieData.writeToXCFile()
FEcase= xc.FEProblem()
FEcase.title= 'Test'
execfile(ieData.getXCFileName())
# Problem type
preprocessor=FEcase.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) 

# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)
oh.displayBlocks()
