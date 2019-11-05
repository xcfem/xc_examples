execfile('./xc_model.py')
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

defDisplay= vtk_CAD_graphic.RecordDefDisplayCAD()
setDisp= xcTotalSet
defDisplay.displayBlocks(setDisp,caption= setDisp.name+' set')
