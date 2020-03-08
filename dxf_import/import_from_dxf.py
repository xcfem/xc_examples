# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from import_export import dxf_reader
from import_export import neutral_mesh_description as nmd

#layerNamesToImport= ['3rd_floor_truss_II.*']
layerNamesToImport= ['2nd_floor']
#layerNamesToImport= ['facade_wall.*']

def getRelativeCoo(pt):
  return [pt[0],pt[1],pt[2]] #No modification.

fileName= 'dxf_model_rev01.dxf'
#fileName= '2nd_floor_ramp_area.dxf'
#fileName= 'pp.dxf'
dxfImport= dxf_reader.DXFImport(fileName, layerNamesToImport,getRelativeCoo, threshold= 0.1,importLines= False, polylinesAsSurfaces= True, tolerance= .25)

#Block topology
blocks= dxfImport.exportBlockTopology('test')

fileName= 'xc_model_blocks'
ieData= nmd.XCImportExportData()
ieData.outputFileName= fileName
ieData.problemName= 'test'
ieData.blockData= blocks

ieData.writeToXCFile()
