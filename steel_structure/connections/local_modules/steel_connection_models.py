# -*- coding: utf-8 -*-
from __future__ import division 
from __future__ import print_function

import math
import geom
import xc

from model.geometry import grid_model as gm
from materials import typical_materials as tm
from model.mesh import finit_el_model as fem
from misc_utils import data_struct_utils as dsu
from model.sets import sets_mng as sets
from connections.steel_connections import cbfem_bolt_weld as sc
from model.sets import sets_mng as sets
from misc_utils import data_struct_utils as dsu
# ---------------------------------------------------------
#Classes intended to generate models of baseplates, gussets, ...

class BoltArray(object):
    '''Defines an array of bolts

    :ivar nRows: number of rows (elements run in X direction)
    :ivar nCols: number of columns (elements run in Y direction)
    :ivar rowDist: distance Y between rows
    :ivar colDist: distance X between columns 
    :ivar boltDiam: diameter of the bolt
    :ivar holeDiam: diameter of the hole
    :ivar xCentr: global X-coord. of the centroid of the array 
                  (defaults to 0)
    :ivar yCentr: global Y-coord. of the centroid of the array
                  (defaults to 0)
    :ivar excludeBoltIndex: list of index (i,j) in the array where there is
                       no bolt (defaults to empty list -> all the 
                       elements in array has a bolt
    :ivar anglXaxis: angle (degrees, counterclockwise) between a row and X axis.
                     Defaults to 0 (rows parallel to global X axis)
    '''
    
    def __init__(self,nRows,nCols,rowDist,colDist,boltDiam,holeDiam,xCentr=0.0,yCentr=0.0,anglXaxis=0,excludeBoltIndex=[]):
        self.nRows=nRows
        self.nCols=nCols
        self.rowDist=rowDist
        self.colDist=colDist
        self.boltDiam=boltDiam
        self.holeDiam=holeDiam
        self.xCentr=xCentr
        self.yCentr=yCentr
        self.anglXaxis=math.radians(anglXaxis)
        self.excludeBoltIndex=excludeBoltIndex

    def boltXYLcoord(self,ind):
        '''Return the local coordinates (x,y) of the bolt placed in 
        index ind=(indexI,indexJ) given as parameters 
        (first row and column have indexes 0)

        :param ind: (indexI,indexJ) indexes of the bolt in 
                    the array (row and column)
        '''
        x=round(-((self.nCols-1)*self.colDist)/2.0+ind[1]*self.colDist,3)
        y=round(-((self.nRows-1)*self.rowDist)/2.0+ind[0]*self.rowDist,3)
        return (x,y)

    def boltXYcoord(self,ind):
        '''Return the global coordinates (x,y) of the bolt placed in 
        index ind=(indexI,indexJ) given as parameters 
        (first row and column have indexes 0)

        :param ind: (indexI,indexJ) indexes of the bolt in 
                    the array (row and column)
        '''
        (xL,yL)=self.boltXYLcoord(ind)  #local coord.
        x=round(self.xCentr+xL*math.cos(self.anglXaxis)-yL*math.sin(self.anglXaxis),3)
        y=round(self.yCentr+xL*math.sin(self.anglXaxis)+yL*math.cos(self.anglXaxis),3)
        return (x,y)

    def getXYcorners(self):
        '''Return a list with the global coordinates (x,y) of the four
        corner bolts
        '''
        (x1,y1)=self.boltXYcoord((self.nCols-1,self.nRows-1))
        (x2,y2)=self.boltXYcoord((0,self.nRows-1))
        (x3,y3)=self.boltXYcoord((0,0))
        (x4,y4)=self.boltXYcoord((self.nCols-1,0))
        return [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
        
    def getXmin(self):
        '''Return the minimum global X coordinate of the array of bolts
        '''
        xCorners=[coo[0] for coo in self.getXYcorners()]
        return min(xCorners)

    def getXmax(self):
        '''Return the maximum global X coordinate of the array of bolts
        '''
        xCorners=[coo[0] for coo in self.getXYcorners()]
        return max(xCorners)

    def getYmin(self):
        '''Return the minimum Y coordinate of the array of bolts
        '''
        yCorners=[coo[1] for coo in self.getXYcorners()]
        return min(yCorners)


    def getYmax(self):
        '''Return the maximum Y coordinate of the array of bolts
        '''
        yCorners=[coo[1] for coo in self.getXYcorners()]
        return max(yCorners)
    
    def getBoltIndexes(self):
        '''Return the list of indexes (i,j) in the array where there is 
        bolt.
        '''
        boltIndex=[(i,j) for i in range(self.nRows) for j in range(self.nCols)]
        for indExcl in self.excludeBoltIndex:
            boltIndex.remove(indExcl)
        return boltIndex

    def getPntHole(self,prep,ind):
        '''Generate the 8 points of a hole for bolt in index ind=(i,j).
        Those points belong to a circle of diameter holeDiam, are 
        qually spaced starting at angle 0 and ordered counterclockwise.

        A list of ordered points is returned. Start point is added to the list
        again on last position to close the circle.

        '''
        lstPnt=list()
        points= prep.getMultiBlockTopology.getPoints
        R=self.holeDiam/2.0
        (xbolt,ybolt)=self.boltXYcoord(ind)
        for i in range(8):
            ang=math.radians(i*45)
            pnt=points.newPntFromPos3d(geom.Pos3d(xbolt+R*math.cos(ang),ybolt+R*math.sin(ang),0))
            lstPnt.append(pnt)
        lstPnt.append(lstPnt[0])
        return lstPnt
            
class BoltPlate(object):
    '''Basic class to create a bolt plate of contour defined by width and height, centered in (0,0).

    :ivar width: width of the steel plate (X direction)
    :ivar height: height of the steel plate (Y direction)
    :ivar boltArray: instance of class BoltArray defining an array of 
                     bolts
    :ivar squareSide: side of the square centered in each bolt to 
                      open the mesh
    :ivar setName: name of the set 
    :ivar tolerance: minimum distance between grid lines
                     (defaults to 0.015)
    :ivar minContSize: minimum size of the plate contour around the 
                       bolt-squares array layout  (not used)
    '''

    def __init__(self,width,height,boltArray,squareSide,setName,tolerance=0.015,minContSize=0.015):
        self.width=width
        self.height=height
        self.boltArray=boltArray
        self.squareSide=squareSide
        self.minContSize=minContSize
        self.setName=setName
        self.tol=tolerance
        self.grid=None
        self.partSet=None
        self.dictPntsBoltHole=dict()
        
    def checkSqSide(self):
        '''Check the bolt-square side to meet the minimum distance to the
        contour of the plate. 
        '''
        xmaxCont=self.width/2.-self.minContSize
        xminCont=-self.width/2.+self.minContSize
        ymaxCont=self.height/2.-self.minContSize
        yminCont=-self.height/2.+self.minContSize
        self.squareSide=min(self.squareSide,
                            2*(xmaxCont-self.boltArray.getXmax()),
                            2*(self.boltArray.getXmin()-xminCont),
                            2*(ymaxCont-self.boltArray.getYmax()),
                            2*(self.boltArray.getYmin()-yminCont),
                            self.boltArray.rowDist-self.minContSize,
                            self.boltArray.colDist-self.minContSize)
        
    def generateGridPoints(self,prep,xList2Add=[],yList2Add=[]):
        '''Create the grid with the basic points (contour of the shape) and 
        those points defined by the coordinates in xList2Add, yList2Add and 
        zList2Add (all the three defaults to empty list)
        Create the part set and append to it all grid points
        '''
        self.halfSqrSide=round(self.squareSide/2.,2)
        xList=[-self.width/2.,self.width/2.]+xList2Add
        yList=[-self.height/2.,self.height/2.]+yList2Add
        for ind in self.boltArray.getBoltIndexes():
            (xBolt,yBolt)=self.boltArray.boltXYcoord(ind)
            coor=round(xBolt-self.halfSqrSide,3)
            if abs(coor-dsu.get_closest_inlist(xList,coor))>self.tol: xList.append(coor)
            if abs(xBolt-dsu.get_closest_inlist(xList,xBolt))>self.tol: xList.append(xBolt)
            coor=round(xBolt+self.halfSqrSide,3)
            if abs(coor-dsu.get_closest_inlist(xList,coor))>self.tol: xList.append(coor)
            coor=round(yBolt-self.halfSqrSide,3)
            if abs(coor-dsu.get_closest_inlist(yList,coor))>self.tol: yList.append(coor)
            if abs(yBolt-dsu.get_closest_inlist(yList,yBolt))>self.tol: yList.append(yBolt)
            coor=round(yBolt+self.halfSqrSide,3)
            if abs(coor-dsu.get_closest_inlist(yList,coor))>self.tol: yList.append(coor)
        xList.sort()
        yList.sort()
        zList=[0]
        xList.sort()
        yList.sort()
        lastXpos=len(xList)-1 ; lastYpos=len(yList)-1 ;  lastZpos=len(zList)-1 
        self.grid= gm.GridModel(prep,xList,yList,zList)
        self.grid.generatePoints()
        self.partSet=prep.getSets.defSet(self.setName)
        pnts=self.partSet.getPoints
        for p in self.grid.getLstPntRange(gm.IJKRange((0,0,0),(lastXpos,lastYpos,lastZpos))):
            pnts.append(p)

    def generateSurfaces(self,prep):
        '''Generate the set of surfaces perforated by the holes
        '''
        if not self.grid:
            self.generateGridPoints(prep)
        lastXpos=len(self.grid.gridCoo[0])-1
        lastYpos=len(self.grid.gridCoo[1])-1

        surfaces=prep.getMultiBlockTopology.getSurfaces
#        self.checkSqSide()
        auxSetTot=self.grid.genSurfOneRegion(gm.IJKRange((0,0,0),(lastXpos,lastYpos,0)),'auxSetTot')
        surfSqRgXYZ=list()
        bltInd=self.boltArray.getBoltIndexes() #squares with bolts
        for ind in bltInd:
            (xmin,xmax,ymin,ymax)=self.getLimSquare(ind)
            surfSqRgXYZ.append([(xmin,ymin,0),(xmax,ymax,0)])
        auxSetSqr=self.grid.genSurfMultiXYZRegion(surfSqRgXYZ,'auxSetSqr')
        for s in auxSetTot.getSurfaces:
            if s not in auxSetSqr.getSurfaces:
                self.partSet.getSurfaces.append(s)
        auxSetTot.clear()
        auxSetSqr.clear()
        #squares with bolts
#        bltInd=self.boltArray.getBoltIndexes()
        for ind in bltInd:
            pntSquare,pntHole=self.getPntSurfHole(prep,ind)
            for i in range(len(pntSquare)-1):
                s=surfaces.newQuadSurfacePts(pntHole[i].tag,pntSquare[i].tag,pntSquare[i+1].tag,pntHole[i+1].tag)
                self.partSet.getSurfaces.append(s)
        self.partSet.fillDownwards()

    def generateMesh(self,prep,thickness,steelMat,eSize):
        if not self.partSet:
            self.generateSurfaces(prep)
        self.mat=tm.DeckMaterialData(name=self.setName+'_mat',thickness=thickness,material=steelMat)
        self.mat.setupElasticSection(prep)
        self.meshpar=fem.SurfSetToMesh(surfSet=self.partSet,matSect=self.mat,elemSize=eSize,elemType='ShellMITC4')
        fem.multi_mesh(prep,[self.meshpar])
        
    def getPntSurfHole(self,prep,ind):
        '''Capture the points in the square others than those that 
        belong to the octagon and creates the analogous points in the 
        hole perimeter. Add those points to the two lists of points
        pntSquare and pntHole that will be used to create the surfaces
        surrounding each hole.
        '''
        points= prep.getMultiBlockTopology.getPoints
        (xbolt,ybolt)=self.boltArray.boltXYcoord(ind)
        dictKey=str(ind[0])+'-'+str(ind[1])
        pntBolt=self.grid.getPntXYZ((xbolt,ybolt,0))
        R=self.boltArray.holeDiam/2.0
        pntSquare=self.getPntSquare(ind)
        pntHole=self.boltArray.getPntHole(prep,ind)
        self.dictPntsBoltHole[dictKey]=[pntBolt,pntHole[0:8]]
        indPntSquare=self.getGridIndPntSquare(ind)
        incrAng=math.radians(45)
        Sqtags=[p.tag for p in pntSquare]
        np=0 ; ang=0
        for p in range(8):
            pnt0=pntSquare[np]
            posPnt0=pnt0.getPos
            indIpnt1=indPntSquare[np][0]
            indIpnt2=indPntSquare[np+1][0]
            indJpnt1=indPntSquare[np][1]
            indJpnt2=indPntSquare[np+1][1]
            indKpnt1=indPntSquare[np][2]
            indKpnt2=indPntSquare[np+1][2]
            if abs(indIpnt1-indIpnt2)>1:
                if indIpnt2>indIpnt1: r=range(indIpnt1+1,indIpnt2)
                else: r=range(indIpnt1-1,indIpnt2,-1)
                for i in r:
                    pntSqIns=self.grid.getPntGrid((i,indJpnt1,indKpnt1))
                    posPntSqIns=pntSqIns.getPos
                    relatDist=posPnt0.dist(posPntSqIns)/self.halfSqrSide
                    angPnt=ang+relatDist*incrAng
                    pntHoleIns=points.newPntFromPos3d(geom.Pos3d(xbolt+R*math.cos(angPnt),ybolt+R*math.sin(angPnt),0))
                    pntSquare.insert(np+1,pntSqIns)
                    pntHole.insert(np+1,pntHoleIns)
                    indPntSquare.insert(np+1,'O')
                    np+=1
            if abs(indJpnt1-indJpnt2)>1:
                if indJpnt2>indJpnt1: r=range(indJpnt1+1,indJpnt2)
                else: r=range(indJpnt1-1,indJpnt2,-1)
                for j in r:
                    pntSqIns=self.grid.getPntGrid((indIpnt1,j,indKpnt1))
                    posPntSqIns=pntSqIns.getPos
                    relatDist=posPnt0.dist(posPntSqIns)/self.halfSqrSide
                    angPnt=ang+relatDist*incrAng
                    pntHoleIns=points.newPntFromPos3d(geom.Pos3d(xbolt+R*math.cos(angPnt),ybolt+R*math.sin(angPnt),0))
                    pntSquare.insert(np+1,pntSqIns)
                    pntHole.insert(np+1,pntHoleIns)
                    indPntSquare.insert(np+1,'O')
                    np+=1
            Sqtags=[p.tag for p in pntSquare]
            np+=1
            ang+=incrAng
        return pntSquare,pntHole
            
    def getLimSquare(self,ind):
        '''Return the limit coordinates (xmin,xmax,ymin,ymax) of the square surrounding 
        a bolt with index in the array of bolts ind=(i,j)
        '''
        (xBolt,yBolt)=self.boltArray.boltXYcoord(ind)
        xmin=round(xBolt-self.halfSqrSide,3)
        xmax=round(xBolt+self.halfSqrSide,3)
        ymin=round(yBolt-self.halfSqrSide,3)
        ymax=round(yBolt+self.halfSqrSide,3)
        return (xmin,xmax,ymin,ymax)              


    def getPntSquare(self,ind):
        '''Return an ordered list of points in the square surrounding 
        a bolt with index in the array of bolts ind=(i,j)
        The last point is a duplicate of initial point to close the circle.

        List starts with point at angle 0 and is ordered counterclockwise.
        '''
        (xBolt,yBolt)=self.boltArray.boltXYcoord(ind)
        (xmin,xmax,ymin,ymax)=self.getLimSquare(ind)
        pnt1=self.grid.getPntXYZ((xmax,yBolt,0))
        pnt2=self.grid.getPntXYZ((xmax,ymax,0))
        pnt3=self.grid.getPntXYZ((xBolt,ymax,0))
        pnt4=self.grid.getPntXYZ((xmin,ymax,0))
        pnt5=self.grid.getPntXYZ((xmin,yBolt,0))
        pnt6=self.grid.getPntXYZ((xmin,ymin,0))
        pnt7=self.grid.getPntXYZ((xBolt,ymin,0))
        pnt8=self.grid.getPntXYZ((xmax,ymin,0))
        return [pnt1,pnt2,pnt3,pnt4,pnt5,pnt6,pnt7,pnt8,pnt1]
    
    def getGridIndPntSquare(self,ind):
        '''Return an ordered list of indexes (i,j,k) in the grid 
        of the points in the square surrounding 
        a bolt with index in the array of bolts ind=(i,j)
        The last point is a duplicate of initial point to close the circle.

        List starts with point at angle 0 and is ordered counterclockwise.
        '''
        (xBolt,yBolt)=self.boltArray.boltXYcoord(ind)
        (xmin,xmax,ymin,ymax)=self.getLimSquare(ind)
        indPnt1=self.grid.getIJKfromXYZ((xmax,yBolt,0))
        indPnt2=self.grid.getIJKfromXYZ((xmax,ymax,0))
        indPnt3=self.grid.getIJKfromXYZ((xBolt,ymax,0))
        indPnt4=self.grid.getIJKfromXYZ((xmin,ymax,0))
        indPnt5=self.grid.getIJKfromXYZ((xmin,yBolt,0))
        indPnt6=self.grid.getIJKfromXYZ((xmin,ymin,0))
        indPnt7=self.grid.getIJKfromXYZ((xBolt,ymin,0))
        indPnt8=self.grid.getIJKfromXYZ((xmax,ymin,0))
        return [indPnt1,indPnt2,indPnt3,indPnt4,indPnt5,indPnt6,indPnt7,indPnt8,indPnt1]
    

class RectPlate(BoltPlate):
    '''Create a rectangular plate perfored with holes,
    centered in (0,0) global coordinates

    :ivar width: width of the steel plate (X direction)
    :ivar height: height of the steel plate (Y direction)
    :ivar boltArray: instance of class BoltArray defining an array of 
                     bolts
    :ivar squareSide: side of the square centered in each bolt to 
                      open the mesh
    :ivar  setName: name of the set
    :ivar tolerance: minimum distance between grid lines
                     (defaults to 0.015)
    :ivar minContSize: minimum size of the plate contour around the 
                       bolt-squares array layout (for now not used
                       because some problems arrive when the geometry
                       is not regular).
    '''

    def __init__(self,width,height,boltArray,squareSide,setName,tolerance=0.015,minContSize=0.015):
        super(RectPlate,self).__init__(width,height,boltArray,squareSide,setName,tolerance,minContSize)



class Gusset1Chamfer(BoltPlate):
    '''Create a gusset plate with one chamfer, perfored with holes.
    The corner opposite to chamfer is placed in (0,0) global coordinates

    :ivar width: total width of the steel plate (X direction)
    :ivar height: total height of the steel plate (Y direction)
    :LxChamfer: length of the chamfer in X direction
    :LyChamfer: length of the chamfer in Y direction
    :ivar boltArray: instance of class BoltArray defining an array of 
                     bolts
    :ivar squareSide: side of the square centered in each bolt to 
                      open the mesh
    :ivar setName: set name
    :ivar tolerance: minimum distance between grid lines
                     (defaults to 0.015)
    :ivar minContSize: minimum size of the plate contour around the 
                       bolt-squares array layout (for now not used
                       because some problems arrive when the geometry
                       is not regular).
    '''
    def __init__(self,width,height,LxChamfer,LyChamfer,boltArray,squareSide,setName,tolerance=0.015,minContSize=0.015):
        self.LxChamfer=LxChamfer
        self.LyChamfer=LyChamfer
        super(Gusset1Chamfer,self).__init__(width,height,boltArray,squareSide,setName,tolerance,minContSize)

    def generateSurfaces(self,prep):
        xChamfer=round(self.width/2-self.LxChamfer,3)
        angChamfer=math.atan(self.LyChamfer/self.LxChamfer)
        yChamfer=round(self.height/2-5/4.*self.LyChamfer,3)
        self.generateGridPoints(prep,xList2Add=[xChamfer],yList2Add=[yChamfer])
        xList=self.grid.gridCoo[0]
        yList=self.grid.gridCoo[1]
        lastXpos=len(xList)-1
        lastYpos=len(yList)-1
        
        indXChamfer=xList.index(xChamfer)
        indYChamfer=yList.index(yChamfer)
        Hmax=yList[-1]-yChamfer
        for i in range(indXChamfer,lastXpos+1):
            Lx=xList[i]-xChamfer
            H=Hmax-math.tan(angChamfer)*Lx
            scale=H/Hmax
            rg=gm.IJKRange((i,indYChamfer,0),(i,lastYpos,0))
            self.grid.scaleCoorYPointsRange(rg,yChamfer,scale)
        super(Gusset1Chamfer,self).generateSurfaces(prep)    
                              
        
class diagPlateForGusset(BoltPlate):
    '''Create a suitable rectangular plate that joints a diagonal and a gusset 
    w/ 1 chamfer given as parameter.

    :ivar gusset: instance of class Gusset1Chamfer
    :ivar width: width of the steel plate (X direction)
    :ivar height: height of the steel plate (Y direction)
    :ivar xCentrBolts: global X-coord. of the centroid of the array of bolts
    :ivar yCentrBolts: global Y-coord. of the centroid of the array of bolts
    :ivar squareSide: side of the square centered in each bolt to 
                      open the mesh
    :ivar setName: name of the set
    :ivar tolerance: minimum distance between grid lines
                     (defaults to 0.015)
    '''
    def __init__(self,gusset,width,height,xCentrBolts,yCentrBolts,squareSide,setName,tolerance=0.015):
        gb=gusset.boltArray
        boltArray=BoltArray(gb.nRows,gb.nCols,gb.rowDist,gb.colDist,gb.boltDiam,gb.holeDiam,xCentrBolts,yCentrBolts,0,gb.excludeBoltIndex)
        self.gussetBolts=gb
        super(diagPlateForGusset,self).__init__(width,height,boltArray,squareSide,setName,tolerance)

    def generateSurfaces(self,prep):
        '''Generate the set of surfaces perforated by the holes
        '''
        super(diagPlateForGusset,self).generateSurfaces(prep)
        deltaDisp=(self.gussetBolts.xCentr-self.boltArray.xCentr,
                   self.gussetBolts.yCentr-self.boltArray.yCentr,
                   0)
#        (x0g,y0g)=self.gussetBolts.boltXYcoord(self.gussetBolts.getBoltIndexes()[0])
#        (x0b,y0b)=self.boltArray.boltXYcoord(self.boltArray.getBoltIndexes()[0])
#        deltaDisp=(x0g-x0b,y0g-y0b,0)
        sets.translat(self.partSet,deltaDisp)
        rotAxis=geom.Line3d(geom.Pos3d(self.gussetBolts.xCentr,self.gussetBolts.yCentr,0.0), geom.Pos3d(self.gussetBolts.xCentr,self.gussetBolts.yCentr,100.0))
        rot=xc.Rotation(geom.Rotation3d(rotAxis,self.gussetBolts.anglXaxis))
        self.partSet.transforms(rot)
        
               
class Icolumn(object):
    '''Create an I-shaped column with axis in global-Z direction 
    passing through global coord. origin. Flanges are oriented 
    in X-direction.

    :ivar height: overall height of the I section
    :ivar flWidht: flange width
    :ivar webThick: web thickness
    :ivar flThick: flange thickness
    :ivar membL: length of the column
    :ivar setName: base name for the sets
    '''
    def __init__(self,height,flWidht,webThick,flThick,membL,setName):
        self.height=height
        self.flWidht=flWidht
        self.webThick=webThick
        self.flThick=flThick
        self.membL=membL
        self.setName=setName
        self.halfFlWidth=round(self.flWidht/2.,3)
        self.halfH=round((self.height-self.flThick)/2.,3)
        self.grid=None
        self.flXnegSet=None
        self.flXposSet=None
        self.webSet=None

    def generateGridPoints(self,prep,xList2Add=[],yList2Add=[],zList2Add=[]):
        '''Create the grid with the basic points (contour of the shape) and 
        those points defined by the coordinates in xList2Add, yList2Add and 
        zList2Add (all the three defaults to empty list)
        '''
        xList=[-self.halfFlWidth,0,self.halfFlWidth]+xList2Add
        yList=[-self.halfH,0,self.halfH]+yList2Add
        zList=[0,self.membL]+zList2Add
        xList.sort() ; yList.sort() ; zList.sort()
        self.grid= gm.GridModel(prep,xList,yList,zList)
        self.grid.generatePoints()
        
    def generateSurfaces(self,prep):
        '''Create sets of surfaces flXnegSet, flXposSurfSet and
        webSurfSet to generate the flange in negative X, 
        the flange in positive X and the web of the column,
        respectively
        '''
        if not self.grid:
            self.generateGridPoints(prep)
        lastXpos=len(self.grid.gridCoo[0])-1
        lastYpos=len(self.grid.gridCoo[1])-1
        lastZpos=len(self.grid.gridCoo[2])-1
        surfaces=prep.getMultiBlockTopology.getSurfaces
        self.flXnegSet=self.grid.genSurfOneRegion(gm.IJKRange((0,0,0),(lastXpos,0,lastZpos)),self.setName+'flXneg')
        self.flXposSet=self.grid.genSurfOneRegion(gm.IJKRange((0,lastYpos,0),(lastXpos,lastYpos,lastZpos)),self.setName+'flXpos')
        self.webSet=self.grid.genSurfOneXYZRegion(((0,-self.halfH,0),(0,self.halfH,self.membL)), self.setName+'web')        

    def generateMesh(self,prep,steelMat,eSize):
        if not self.webSet:
            self.generateSurfaces(prep)
        flange_mat=tm.DeckMaterialData(name='flange_mat',thickness= self.flThick,material=steelMat)
        flange_mat.setupElasticSection(prep)
        web_mat=tm.DeckMaterialData(name='web_mat',thickness= self.webThick,material=steelMat)
        web_mat.setupElasticSection(prep)
        flXneg_mesh=fem.SurfSetToMesh(surfSet=self.flXnegSet,matSect=flange_mat,elemSize=eSize,elemType='ShellMITC4')
        flXpos_mesh=fem.SurfSetToMesh(surfSet=self.flXposSet,matSect=flange_mat,elemSize=eSize,elemType='ShellMITC4')
        web_mesh=fem.SurfSetToMesh(surfSet=self.webSet,matSect=web_mat,elemSize=eSize,elemType='ShellMITC4')
        fem.multi_mesh(preprocessor=prep,lstMeshSets=[flXneg_mesh,flXpos_mesh,web_mesh],sectGeom='N') 


class ColumnBaseConnection(object):
    '''Assembly a steel column, a base plate and one or two diagonals
     
    :ivar column: column object
    :ivar basePlate: base plate object
    :ivar gussetFlange: gusset object glued to the flange of the column
    :ivar diagPlateGussetFlange: plate that joints a diagonal and the gussetFlange
    :ivar gussetWeb: gusset object glued to the web of the column
    :ivar diagPlateGussetWeb: plate that joints a diagonal and the gussetWeb
    '''
     
    def __init__(self,column,basePlate,gussetFlange=None,diagPlateGussetFlange=None,gussetWeb=None,diagPlateGussetWeb=None):
        self.column=column
        self.basePlate=basePlate
        self.gussetFlange=gussetFlange
        self.diagPlateGussetFlange=diagPlateGussetFlange
        self.gussetWeb=gussetWeb
        self.diagPlateGussetWeb=diagPlateGussetWeb

            
    def generateMesh(self,prep,steelColumn,steelBasePlate,steelGussets,thickPasePlate,thickGussetFlange,thickDiagPlateGussetFlange,thickGussetWeb,thickDiagPlateGussetWeb,eSize):
        '''Assembly the elements and generate the mesh
        '''
        self.column.generateMesh(prep,steelColumn,eSize)
        self.basePlate.generateMesh(prep,thickPasePlate,steelBasePlate,eSize)
        if self.gussetFlange:
            self.gussetFlange.generateSurfaces(prep)
            if self.diagPlateGussetFlange:
                self.diagPlateGussetFlange.generateSurfaces(prep)
            sets.rot_X(self.gussetFlange.partSet,90)
            sets.rot_Z(self.gussetFlange.partSet,90)
            dy=self.column.height/2+self.gussetFlange.width/2.
            dz=self.gussetFlange.height/2.
            sets.translat(self.gussetFlange.partSet,(0,dy,dz))
            if self.diagPlateGussetFlange:
                sets.rot_X(self.diagPlateGussetFlange.partSet,90)
                sets.rot_Z(self.diagPlateGussetFlange.partSet,90)
                sets.translat(self.diagPlateGussetFlange.partSet,(thickGussetFlange/2.+thickDiagPlateGussetFlange/2.,dy,dz))
                self.diagPlateGussetFlange.generateMesh(prep,thickDiagPlateGussetFlange,steelGussets,eSize)

            self.gussetFlange.generateMesh(prep,thickGussetFlange,steelGussets,eSize)
        if self.gussetWeb:
            self.gussetWeb.generateSurfaces(prep)
            if self.diagPlateGussetWeb:
                self.diagPlateGussetWeb.generateSurfaces(prep)
            sets.rot_X(self.gussetWeb.partSet,90)
            dx=self.gussetWeb.width/2.
            dz=self.gussetWeb.height/2.
            sets.translat(self.gussetWeb.partSet,(dx,0,dz))
            if self.diagPlateGussetWeb:
                sets.rot_X(self.diagPlateGussetWeb.partSet,90)
                sets.translat(self.diagPlateGussetWeb.partSet,(dx,thickGussetWeb/2.+thickDiagPlateGussetWeb/2.,dz))
                self.diagPlateGussetWeb.generateMesh(prep,thickDiagPlateGussetWeb,steelGussets,eSize)
            self.gussetWeb.generateMesh(prep,thickGussetWeb,steelGussets,eSize)

            
#avlbWeldSz=[4e-3,5e-3,6e-3,7e-3,8e-3,9e-3,10e-3,11e-3,12e-3,13e-3,14e-3]  #available weld sizes
class HSSmember(object):
    ''' Creates a horizontal HSS member.
    The longitudinal axis of the member follows the direction of the positive 
    X axis in the grid, the start point is placed at grid coordinates (0,0,0),
    The member is placed at its position in global coord. system making use 
    of attributes vCentr and angX.

    :ivar shape: steel HSS shape (ex: ASTM_materials.HSSShape)
    :ivar L: length of the member
    :ivar vOrig: xc.Vector representing the global coordinates of the point 
                 where to place the point of the beam-axis in its initial extremity
    :ivar angX: angle between the global X-axis and the axis of the beam (degrees)
    :ivar idName: id to give a name to the set
    :ivar bevelWidth: if True creates a bevel with angle angX in the width of 
                      the shape at the start of the beam (defaults to False)
    :ivar bevelHeight: if True creates a bevel with angle angX in the height of 
                      the shape at the start of the beam (defaults to False)
    '''
    def __init__(self,shape,L,vOrig,angX,idName,rotX=False,rotY=False,bevelWidth=False,bevelHeight=False):
        self.shape=shape
        self.L=L
        self.vOrig=vOrig
        self.angX=angX
        self.idName=idName
        self.rotX=rotX
        self.rotY=rotY
        self.bevelWidth=bevelWidth
        self.bevelHeight=bevelHeight
        self.member=None
        
    def genSurfaces(self,modelSpace):
        xList=[0,self.L]
        wdth=self.shape.b()-self.shape.t()
        hgth=self.shape.h()-self.shape.t()
        yList=[-wdth/2,0,wdth/2]
        zList=[-hgth/2,0,hgth/2]
        self.grid=gm.GridModel(modelSpace.preprocessor,xList,yList,zList)
        self.grid.generatePoints()
        if self.rotX:
            self.grid.rotAllPntsXAxis(self.rotX,[0,0])
        if self.rotY:
            self.grid.rotAllPntsYAxis(self.rotY,[0,0])
        if self.bevelWidth:
            extrPnts=self.grid.getSetPntXYZRange(((0,-wdth/2,-hgth/2),(0,wdth/2,hgth/2)),'extrPnts')
            tgAng=math.tan(math.radians(self.angX))
            for p in extrPnts.points:
                y=p.getPos.y
                deltaX=-y/tgAng
                p.getPos.x+=deltaX
            extrPnts.clear()    
        if self.bevelHeight:
            extrPnts=self.grid.getSetPntXYZRange(((0,-wdth/2,-hgth/2),(0,wdth/2,hgth/2)),'extrPnts')
            tgAng=math.tan(math.radians(self.angX))
            for p in extrPnts.points:
                z=p.getPos.z
                deltaX=-z/tgAng
                p.getPos.x+=deltaX
            extrPnts.clear()    
        self.grid.rotAllPntsZAxis(self.angX,[0,0])
        self.grid.moveAllPoints(self.vOrig)
        setName=self.idName+'member'
        self.member=self.grid.genSurfMultiXYZRegion([
            ((0,-wdth/2,-hgth/2),(self.L,-wdth/2,hgth/2)),
            ((0,wdth/2,-hgth/2),(self.L,wdth/2,hgth/2)),
            ((0,-wdth/2,-hgth/2),(self.L,wdth/2,-hgth/2)),
            ((0,-wdth/2,hgth/2),(self.L,wdth/2,hgth/2))],setName)
    
    def genMesh(self,modelSpace,memberMat,esize):
        if not self.member:
            self.genSurfaces(modelSpace)
        member_mesh=fem.SurfSetToMesh(surfSet=self.member,matSect=memberMat,elemSize=esize,elemType='ShellMITC4')
        fem.multi_mesh(modelSpace.preprocessor,[member_mesh])

    def genWeldTopInitExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((0,-self.shape.b()/2,self.shape.h()/2))
        p2=self.grid.getPntXYZ((0,self.shape.b()/2,self.shape.h()/2))
        w=auxgenWeld([p1,p2],self.member,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldBottInitExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=-1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((0,-self.shape.b()/2,-self.shape.h()/2))
        p2=self.grid.getPntXYZ((0,self.shape.b()/2,-self.shape.h()/2))
        w=auxgenWeld([p1,p2],self.member,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldLeftInitExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=-1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((0,-self.shape.b()/2,-self.shape.h()/2))
        p2=self.grid.getPntXYZ((0,-self.shape.b()/2,self.shape.h()/2))
        w=auxgenWeld([p1,p2],self.member,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldRightInitExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((0,self.shape.b()/2,-self.shape.h()/2))
        p2=self.grid.getPntXYZ((0,self.shape.b()/2,self.shape.h()/2))
        w=auxgenWeld([p1,p2],self.member,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldContourInitExtr(self,weldType,toSet,toSetSign=1,weldDescrip=''):
        lstWelds=list()
        weldSetName=self.idName+'WinitTop'
        lstWelds.append(self.genWeldTopInitExtr(weldType,toSet,weldSetName,toSetSign,weldDescrip=weldDescrip))
        weldSetName=self.idName+'WinitBott'
        lstWelds.append(self.genWeldBottInitExtr(weldType,toSet,weldSetName,toSetSign,weldDescrip=weldDescrip))
        weldSetName=self.idName+'WinitLeft'
        lstWelds.append(self.genWeldLeftInitExtr(weldType,toSet,weldSetName,toSetSign,weldDescrip=weldDescrip))
        weldSetName=self.idName+'WinitRight'
        lstWelds.append(self.genWeldRightInitExtr(weldType,toSet,weldSetName,toSetSign,weldDescrip=weldDescrip))
        return lstWelds
    
    def genWeldTopEndExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((self.L,-self.shape.b()/2,self.shape.h()/2))
        p2=self.grid.getPntXYZ((self.L,self.shape.b()/2,self.shape.h()/2))
        w=auxgenWeld([p1,p2],self.member,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldBottEndExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=-1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((self.L,-self.shape.b()/2,-self.shape.h()/2))
        p2=self.grid.getPntXYZ((self.L,self.shape.b()/2,-self.shape.h()/2))
        w=auxgenWeld([p1,p2],self.member,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldLeftEndExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=-1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((self.L,-self.shape.b()/2,-self.shape.h()/2))
        p2=self.grid.getPntXYZ((self.L,-self.shape.b()/2,self.shape.h()/2))
        w=auxgenWeld([p1,p2],self.member,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldRightEndExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((self.L,self.shape.b()/2,-self.shape.h()/2))
        p2=self.grid.getPntXYZ((self.L,self.shape.b()/2,self.shape.h()/2))
        w=auxgenWeld([p1,p2],self.member,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldContourEndExtr(self,weldType,toSet,toSetSign=1,weldDescrip=''):
        lstWelds=list()
        weldSetName=self.idName+'WendTop'
        lstWelds.append(self.genWeldTopEndExtr(weldType,toSet,weldSetName,toSetSign,weldDescrip=weldDescrip))
        weldSetName=self.idName+'WendBott'
        lstWelds.append(self.genWeldBottEndExtr(weldType,toSet,weldSetName,toSetSign,weldDescrip=weldDescrip))
        weldSetName=self.idName+'WendLeft'
        lstWelds.append(self.genWeldLeftEndExtr(weldType,toSet,weldSetName,toSetSign,weldDescrip=weldDescrip))
        weldSetName=self.idName+'WendRight'
        lstWelds.append(self.genWeldRightEndExtr(weldType,toSet,weldSetName,toSetSign,weldDescrip=weldDescrip))
        return lstWelds
    
    def fixInitExtr(self,modelSpace):      
        ''' fix displacement DOF in points of the beam initial extremity'''
        fixPnts=self.grid.getSetPntXYZRange(((0,-self.shape.b()/2,-self.shape.h()/2),(0,self.shape.b()/2,self.shape.h()/2)),'fixPnts')
        print('n puntos',fixPnts.points.size)
        fixNodes=[p.getNode() for p in fixPnts.points if p.getNode()]
        fixPnts.clear()
        for n in fixNodes:
            modelSpace.fixNode000_FFF(n.tag)

            
    def fixEndExtr(self,modelSpace):      
        ''' fix displacement DOF in points of the beam end extremity'''
        fixPnts=self.grid.getSetPntXYZRange(((self.L,-self.shape.b()/2,-self.shape.h()/2),(self.L,self.shape.b()/2,self.shape.h()/2)),'fixPnts')
        fixNodes=[p.getNode() for p in fixPnts.points if p.getNode()]
        fixPnts.clear()
        for n in fixNodes:
            modelSpace.fixNode000_FFF(n.tag)
    
    def fixBothExtr(self,modelSpace):      
        ''' fix displacement DOF in points of the beam at both extremities'''
        self.fixInitExtr(modelSpace)
        self.fixEndExtr(modelSpace)
        
 

class Ibeam(object):
    ''' Creates a horizontal I beam.
    The longitudinal axis of the beam follows the direction of the positive 
    X axis in the grid, the start point is placed at grid coordinates (0,0,0),
    and the web of the beam is on grid plane XZ. 
    The beam is placed at its position in global coord. system making use 
    of attributes vCentr and angX.

    :ivar shape: steel I shape (ex: ASTM_materials.WShape)
    :ivar L: length of the beam
    :ivar vOrig: xc.Vector representing the global coordinates of the point 
                 where to place the point of the beam-axis in its initial extremity
    :ivar angX: angle between the global X-axis and the axis of the beam (degrees)
    :ivar idName: id to give names to the sets
    :ivar bevelWidth: if True creates a bevel with angle angX in the width of 
                      the shape at the start of the beam (defaults to False)
    :ivar bevelHeight: if True creates a bevel with angle angX in the height of 
                      the shape at the start of the beam (defaults to False)
    :ivar rotX: angle of rotation around the londitudinal axis in degrees
                (defaults to None)
    :ivar rotY: angle of rotation around the global Y axis in degrees
                (defaults to None)
    :ivar lstXYZBoltCoord: coordinates of the bolts in the the beam,
                expressed in the grid relative coordinate system. 
                (defaults to none bolt)
    :ivar topNotch: True if notch in top-flange (defaults to False)
    :ivar bottNotch: True if notch in bottom-flange (defaults to False)
    :ivar notchDim: dimensions of the notch [length,height]
                    (defaults to [] -> no notch)
   '''
    def __init__(self,shape,L,vOrig,angX,idName,bevelWidth=False,bevelHeight=False,rotX=False,rotY=False,lstXYZBoltCoord=[],topNotch=False,bottNotch=False,notchDim=[]):
        self.shape=shape
        self.L=L
        self.vOrig=vOrig
        self.angX=angX
        self.idName=idName
        self.bevelWidth=bevelWidth
        self.bevelHeight=bevelHeight
        self.rotX=rotX
        self.rotY=rotY
        self.lstXYZBoltCoord=lstXYZBoltCoord
        self.topNotch=topNotch
        self.bottNotch=bottNotch
        self.notchDim=notchDim
        self.topFlange=None
        
    def genSurfaces(self,modelSpace):
        xBolts=[coo[0] for coo in self.lstXYZBoltCoord]
        yBolts=[coo[1] for coo in self.lstXYZBoltCoord]
        zBolts=[coo[2] for coo in self.lstXYZBoltCoord]
        xNotch=[self.notchDim[0]] if (self.topNotch or self.bottNotch) else []
        xList=[0,self.L]+xBolts+xNotch ; xList.sort()
        xList=dsu.remove_duplicates_list(xList)
        yList=[-self.shape.b()/2,0,self.shape.b()/2]+yBolts; yList.sort()
        yList=dsu.remove_duplicates_list(yList)
        self.zFlange=(self.shape.h()-self.shape.tf())/2
        zTopNotch=[self.getZtopWeb()] if self.topNotch  else []
        zBottNotch=[self.getZbottWeb()] if self.bottNotch else []
        zList=[-self.zFlange,0,self.zFlange]+zBolts+zTopNotch+zBottNotch ; zList.sort()
        zList=dsu.remove_duplicates_list(zList)
        self.grid=gm.GridModel(modelSpace.preprocessor,xList,yList,zList)
        self.grid.generatePoints()
        if self.bevelWidth:
            extrPnts=self.grid.getSetPntXYZRange(((0,-self.shape.b()/2,-self.zFlange),(0,self.shape.b()/2,self.zFlange)),'extrPnts')
            tgAng=math.tan(math.radians(self.angX))
            for p in extrPnts.points:
                y=p.getPos.y
                deltaX=-y/tgAng
                p.getPos.x+=deltaX
            extrPnts.clear()
        if self.bevelHeight:
            extrPnts=self.grid.getSetPntXYZRange(((0,-self.shape.b()/2,-self.zFlange),(0,self.shape.b()/2,self.zFlange)),'extrPnts')
            tgAng=math.tan(math.radians(self.angX))
            for p in extrPnts.points:
                z=p.getPos.z
                deltaX=-z/tgAng
                p.getPos.x+=deltaX
            extrPnts.clear()    
        if self.rotX:
            self.grid.rotAllPntsXAxis(self.rotX,[0,0])
        if self.rotY:
            self.grid.rotAllPntsYAxis(self.rotY,[0,0])
        self.grid.rotAllPntsZAxis(self.angX,[0,0])
        self.grid.moveAllPoints(self.vOrig)
        setName=self.idName+'topFlange'
        xInit=xNotch[0] if self.topNotch else 0        
        self.topFlange=self.grid.genSurfOneXYZRegion(
            ((xInit,-self.shape.b()/2,self.zFlange),(self.L,self.shape.b()/2,self.zFlange)),setName)
        setName=self.idName+'bottFlange'
        xInit=xNotch[0] if self.bottNotch else 0
        self.bottFlange=self.grid.genSurfOneXYZRegion(
            ((xInit,-self.shape.b()/2,-self.zFlange),(self.L,self.shape.b()/2,-self.zFlange)),setName)
        setName=self.idName+'web'
        if not(self.topNotch) and not(self.bottNotch):
            web_reg=[ ((0,0,-self.zFlange),(self.L,0,self.zFlange))]
        elif (self.topNotch and self.bottNotch):
            web_reg=[ ((xNotch[0],0,zTopNotch[0]),(self.L,0,self.zFlange)),
                      ((0,0,zBottNotch[0]),(self.L,0,zTopNotch[0])),
                      ((xNotch[0],0,-self.zFlange),(self.L,0,zBottNotch[0]))
                      ]
        elif self.topNotch :
            print('zTopNotch=', zTopNotch[0])
            web_reg=[ ((xNotch[0],0,zTopNotch[0]),(self.L,0,self.zFlange)),
                      ((0,0,-self.zFlange),(self.L,0,zTopNotch[0])),
                      ]
        else:
            web_reg=[ ((0,0,zBottNotch[0]),(self.L,0,self.zFlange)),
                      ((xNotch[0],0,-self.zFlange),(self.L,0,zBottNotch[0]))
                      ]
        self.web=self.grid.genSurfMultiXYZRegion(web_reg,setName)
        setName=self.idName+'beam'
        self.beam=modelSpace.setSum(setName,[self.topFlange,self.bottFlange,self.web])

    def genMesh(self,modelSpace,flangeMat,webMat,esize):
        if not self.topFlange:
            self.genSurfaces(modelSpace)
        topFlange_mesh=fem.SurfSetToMesh(surfSet=self.topFlange,matSect=flangeMat,elemSize=esize,elemType='ShellMITC4')
        bottFlange_mesh=fem.SurfSetToMesh(surfSet=self.bottFlange,matSect=flangeMat,elemSize=esize,elemType='ShellMITC4')
        web_mesh=fem.SurfSetToMesh(surfSet=self.web,matSect=webMat,elemSize=esize,elemType='ShellMITC4')
        fem.multi_mesh(modelSpace.preprocessor,[topFlange_mesh,bottFlange_mesh,web_mesh])
        self.beam.fillDownwards()

    def getZtopWeb(self):
        if not(self.topNotch):
            ztf=self.shape.h()/2-self.shape.tf()/2
        else:
            ztf=self.shape.h()/2+self.shape.tf()/2-self.notchDim[1]
        return ztf

    def getZbottWeb(self):
        if not(self.bottNotch):
            ztf=-self.shape.h()/2+self.shape.tf()/2
        else:
            ztf=-self.shape.h()/2-self.shape.tf()/2+self.notchDim[1]
        return ztf

    def fixInitExtr(self,modelSpace):      
        ''' fix displacement DOF in points of the beam initial extremity'''
        fixPnts=self.grid.getSetPntXYZRange(((0,-self.shape.b()/2,-self.zFlange),(0,self.shape.b()/2,self.zFlange)),'fixPnts')
        print('n puntos',fixPnts.points.size)
        fixNodes=[p.getNode() for p in fixPnts.points if p.getNode()]
        fixPnts.clear()
        for n in fixNodes:
            modelSpace.fixNode000_FFF(n.tag)
    
    def fixEndExtr(self,modelSpace):      
        ''' fix displacement DOF in points of the beam end extremity'''
        fixPnts=self.grid.getSetPntXYZRange(((self.L,-self.shape.b()/2,-self.zFlange),(self.L,self.shape.b()/2,self.zFlange)),'fixPnts')
        fixNodes=[p.getNode() for p in fixPnts.points if p.getNode()]
        fixPnts.clear()
        for n in fixNodes:
            modelSpace.fixNode000_FFF(n.tag)
    
    def fixBothExtr(self,modelSpace):      
        ''' fix displacement DOF in points of the beam at both extremities'''
        self.fixInitExtr(modelSpace)
        self.fixEndExtr(modelSpace)

    def genWeldTopFlangeInitExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((0,-self.shape.b()/2,self.zFlange))
        p2=self.grid.getPntXYZ((0,self.shape.b()/2,self.zFlange))
        w=auxgenWeld([p1,p2],self.topFlange,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w

    def genWeldBottFlangeInitExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((0,-self.shape.b()/2,-self.zFlange))
        p2=self.grid.getPntXYZ((0,self.shape.b()/2,-self.zFlange))
        w=auxgenWeld([p1,p2],self.bottFlange,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w

    def genWeldWebInitExtr(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        zbott=self.getZbottWeb()
        ztop=self.getZtopWeb()
        p1=self.grid.getPntXYZ((0,0,zbott))
        p2=self.grid.getPntXYZ((0,0,ztop))
        w=auxgenWeld([p1,p2],self.web,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w

    def genWeldContourInitExtr(self,weldType,toSet,toSetSign=1,weldDescrip=''):
        lstWelds=list()
        weldSetName=self.idName+'topFlange'
        lstWelds.append(self.genWeldTopFlangeInitExtr(weldType,toSet,weldSetName,toSetSign,bothSides=True,weldDescrip=weldDescrip))
        weldSetName=self.idName+'bottFlange'
        lstWelds.append(self.genWeldBottFlangeInitExtr(weldType,toSet,weldSetName,toSetSign,bothSides=True,weldDescrip=weldDescrip))
        weldSetName=self.idName+'webFlange'
        lstWelds.append(self.genWeldWebInitExtr(weldType,toSet,weldSetName,toSetSign,bothSides=True,weldDescrip=weldDescrip))
        return lstWelds
                        


class rectWeldPlate(object):
    '''Creates a vertical rectangular plate to be welded to other members.
    The center of the plate is located at grid-coord. (0,0,0), width is 
    parallel to the axis X of the grid and height parallel to the grid Z-axis
    The plate is placed at its position in global coord. system making use 
    of attributes vCentr and angX.

    :ivar W: width (X dir)
    :ivar H: height(Z dir)
    :ivar vCentr: xc.Vector representing the global coordinates of the point 
                 where to place the center of the rectangle
    :ivar angX: angle between the global X-axis and the axis of the beam (degrees)
    :ivar idName: id to give names to the sets
    :ivar rotX: angle of rotation around the londitudinal axis in degrees
                (defaults to None)
    '''
    def __init__(self,W,H,vCentr,angX,idName,rotX=None):
        self.W=W
        self.H=H
        self.vCentr=vCentr
        self.angX=angX
        self.idName=idName
        self.rotX=rotX
        self.plate=None
        self.grid=None

    def genPoints(self,modelSpace):
        xList=[-self.W/2,self.W/2]
        yList=[0]
        zList=[-self.H/2,self.H/2]
        self.grid=gm.GridModel(modelSpace.preprocessor,xList,yList,zList)
        self.grid.generatePoints()
        if self.rotX:
            self.grid.rotAllPntsXAxis(self.rotX,[0,0])
        if self.angX !=0: self.grid.rotAllPntsZAxis(self.angX,[0,0])
        self.grid.moveAllPoints(self.vCentr)
        
    def genSurfaces(self,modelSpace):
        if not self.grid:
            self.genPoints(modelSpace)
        setName=self.idName+'plate'
        self.plate=self.grid.genSurfOneXYZRegion(
            ((-self.W/2,0,-self.H/2),(self.W/2,0,self.H/2)),setName)

    def genMesh(self,modelSpace,plateMat,esize):
        if not self.plate:
            self.genSurfaces(modelSpace)
        plate_mesh=fem.SurfSetToMesh(surfSet=self.plate,matSect=plateMat,elemSize=esize,elemType='ShellMITC4')
        fem.multi_mesh(modelSpace.preprocessor,[plate_mesh])

    def genWeldTopEdge(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((-self.W/2,0,self.H/2))
        p2=self.grid.getPntXYZ((self.W/2,0,self.H/2))
        w=auxgenWeld([p1,p2],self.plate,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w


    def genWeldBottomEdge(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((-self.W/2,0,-self.H/2))
        p2=self.grid.getPntXYZ((self.W/2,0,-self.H/2))
        w=auxgenWeld([p1,p2],self.plate,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w
    
    def genWeldLeftEdge(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((-self.W/2,0,-self.H/2))
        p2=self.grid.getPntXYZ((-self.W/2,0,self.H/2))
        w=auxgenWeld([p1,p2],self.plate,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w

    def genWeldRightEdge(self,weldType,toSet,weldSetName,toSetSign=1,bothSides=False,plateSign=1,nDiv=15,weldDescrip=''):
        p1=self.grid.getPntXYZ((self.W/2,0,-self.H/2))
        p2=self.grid.getPntXYZ((self.W/2,0,self.H/2))
        w=auxgenWeld([p1,p2],self.plate,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip)
        return w

    def genWeldVariousEdges(self,weldType,toSet,weldSetName,toSetSign=1,edgesId='TBLR',weldDescrip=''):
        '''Return a list of double welds along the edges of the plate defined by edgesId

        :param weldType: CBfem bolt weld type
        :param toSet: set of elements to which weld the member
        :param weldSetName: name of the set of weld elements created
        :param toSetSign: sign to define the side of the weld in the elements of toSet
                          (defaults to 1:positive side)
        :param edgesId: string to define the edges of the member to be welded ('T' for
                        top edge, 'B' for bottom edge, 'L' for left edge, 'R' for right
                        edge (defaults to 'TBLR'-> all contour)
        :param weldDescrip: description
        '''
        lstWelds=list()
        edgesId=edgesId.upper()
        if 'T' in edgesId:
            weldSetName=self.idName+'WTopEdg'
            lstWelds.append(self.genWeldTopEdge(weldType,toSet,weldSetName,toSetSign,bothSides=True,weldDescrip='weldDescrip'))
        if 'B' in edgesId:
            weldSetName=self.idName+'WBottEdg'
            lstWelds.append(self.genWeldBottomEdge(weldType,toSet,weldSetName,toSetSign,bothSides=True,weldDescrip='weldDescrip'))
        if 'L' in edgesId:
            weldSetName=self.idName+'WLeftEdg'
            lstWelds.append(self.genWeldLeftEdge(weldType,toSet,weldSetName,toSetSign,bothSides=True,weldDescrip='weldDescrip'))
        if 'R' in edgesId:
            weldSetName=self.idName+'WRightEdg'
            lstWelds.append(self.genWeldRightEdge(weldType,toSet,weldSetName,toSetSign,bothSides=True,weldDescrip='weldDescrip'))
        return lstWelds
                            
                            

def auxgenWeld(pairPnt,fromSet,weldType,toSet,weldSetName,toSetSign,bothSides,plateSign,nDiv,weldDescrip):
    l=geom.Segment3d(pairPnt[0].getPos,pairPnt[1].getPos)
    w=sc.MultiFilletWeld(weldType,fromSet,toSet,[l],weldSetName,weldDescrip)
    if bothSides:
        w.generateWeld(nDiv=nDiv,WS2sign=toSetSign,bothSidesOfWS1=True)
    else:
        w.generateWeld(nDiv=nDiv,WS1sign=plateSign,WS2sign=toSetSign,bothSidesOfWS1=False)
    return w
       
        
class rectFakeBoltedPlate(rectWeldPlate):
    '''Creates a vertical rectangular plate to be bolted to other members.
    The center of the plate is located at grid-coord. (0,0,0), width is 
    parallel to the axis X of the grid and height parallel to the grid Z-axis
    The plate is placed at its position in global coord. system making use 
    of attributes vCentr and angX.

    :ivar W: width (X dir)
    :ivar H: height(Z dir)
    :ivar vCentr: xc.Vector representing the global coordinates of the point 
                 where to place the center of the rectangle
    :ivar angX: angle between the global X-axis and the axis of the beam (degrees)
    :ivar idName: id to give names to the sets
    :ivar lstXZBoltCoord: coordinates of the bolts in the grid coordinate 
          system centered in the center of the base plate with 1st coord. 
          horizontal and 2nd coord. vertical
    :ivar rotX: angle of rotation around the londitudinal axis in degrees
                (defaults to None)
    '''
    def __init__(self,W,H,vCentr,angX,idName,lstXZBoltCoord,rotX=None):
        self.lstXZBoltCoord=lstXZBoltCoord
        super(rectFakeBoltedPlate,self).__init__(W,H,vCentr,angX,idName,rotX)

    def genPoints(self,modelSpace):
        xBolts=[coo[0] for coo in self.lstXZBoltCoord]
        zBolts=[coo[1] for coo in self.lstXZBoltCoord]
        xList=[-self.W/2,self.W/2] +xBolts ; xList.sort()
        xList=dsu.remove_duplicates_list(xList)
        yList=[0]
        zList=[-self.H/2,self.H/2]+zBolts ; zList.sort()
        zList=dsu.remove_duplicates_list(zList)
        self.grid=gm.GridModel(modelSpace.preprocessor,xList,yList,zList)
        self.grid.generatePoints()
        if self.rotX:
            self.grid.rotAllPntsXAxis(self.rotX,[0,0])
        self.grid.rotAllPntsZAxis(self.angX,[0,0])
        self.grid.moveAllPoints(self.vCentr)

        
    
    
   
