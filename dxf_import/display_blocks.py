execfile('./xc_model.py')
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

displaySettings= vtk_CAD_graphic.DisplaySettingsBlockTopo()
setDisp= xcTotalSet
displaySettings.displayBlocks(setDisp,caption= setDisp.name+' set')
