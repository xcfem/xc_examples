exec(open('./xc_model.py').read())
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

displaySettings= vtk_CAD_graphic.DisplaySettingsBlockTopo()
setDisp= xcTotalSet
displaySettings.displayBlocks(setDisp,caption= setDisp.name+' set')
