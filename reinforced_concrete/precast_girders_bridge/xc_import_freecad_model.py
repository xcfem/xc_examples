# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from import_export import freecad_reader
from import_export import neutral_mesh_description as nmd

def getRelativeCoo(pt):
    return [pt[0]/1000.0,pt[1]/1000.0,pt[2]/1000.0]

groupsToImport= ['IFC.*']

baseName= './tablero_rev04'
freeCADFileName= baseName+'.FCStd'
freeCADImport= freecad_reader.FreeCADImport(freeCADFileName, groupsToImport, getRelativeCoo, threshold= 0.03)

#Block topology
blocks= freeCADImport.exportBlockTopology('test')

ieData= nmd.XCImportExportData()
ieData.outputFileName= baseName+'_blocks'
#ieData.outputFileName= 'pp.py'
ieData.problemName= 'FEcase'
ieData.blockData= blocks

ieData.writeToXCFile()
