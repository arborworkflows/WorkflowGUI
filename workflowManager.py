
import os
import sys
import threading
import urllib

from PyQt4 import QtCore
from PyQt4 import QtGui

from PyQt4.QtCore import (Qt, SIGNAL,QUrl, pyqtSlot, pyqtSignal, QPoint, QPointF,QRectF,QString)
from PyQt4.QtGui import (QApplication, QDialog, QHBoxLayout, QIcon, QColor, QPainterPath,
        QPainter, QPolygonF, QPen, QBrush, QGraphicsObject,
        QListWidget, QListWidgetItem, QSplitter, QTableWidget, QPushButton, QCursor)
from PyQt4 import QtDeclarative

# globals used to aid visualization.  Below is a table of input and output offset values depending on the type of the 
# workstep.  The Segment class uses this to determine where to draw the edges since the edge just knows which operation 
# it is attached to.  This table must be coordinated with the icon artwork. 

outputOffsets = {QString(u'DataIntegrator') : [140,130], QString(u'endpoint') : [0,0], QString(u'FitContinuous') : [160,105], QString(u'TreeTransform') : [140,105],  QString(u'TreeFromFile') : [155,125], QString(u'OpenTreeOfLife') : [155,125], QString(u'CharacterMatrix') : [155,125]}
inputOffsets = {QString(u'DataIntegrator') : [0,70], 'endpoint' : [0,0], QString(u'FitContinuous') : [5,95], QString(u'TreeTransform') : [5,115]}

# A table of operation types is needed to look back by name to find out the proper operation type and then lookup the index
# This dictionary is filled out as objects are added to the scene.  The Segment class uses this cross-reference to find the 
# types to lookup in the global offset table above.
operationsType = {}

# Switch convenience class definition of a switch statement for python.  This lets us use
# c-like switch options in python methods

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False  
             
# This represents the connection segment used.  There has to be a sourceObject
# and destination object instantiated in order to set positions correctly. 
             
class Segment(QtDeclarative.QDeclarativeItem):

    def __init__(self, color,parent):
        super(Segment, self).__init__(parent)
        print "Segment init"
        self.color = color
        self.change = 1
        self.angle = 0
        self.setFlag(self.ItemHasNoContents,0);

      
    def setSourceObject(self,src):
        self.sourceObject = src

    def setDestinationObject(self,dst):
        self.destinationObject = dst       

    def boundingRect(self):
        # the destination point could be closer or farther from the origin,
        # so return a rectangle that is 2x as big as necessary and will always
        # contain both points.  A fudge of 10 extra border pixels is added to allow for rounded
        # ends of the lines to not cause rendering artifacts
        sizex = abs(self.destinationObject.pos().x()-self.sourceObject.pos().x())
        sizey = abs(self.destinationObject.pos().y()-self.sourceObject.pos().y())
        #print "sizex,sizey= ",sizex, " ",sizey
        rect = QRectF(self.sourceObject.pos().x()-sizex-50,self.sourceObject.pos().y()-sizey-50,2*sizex+20,2*sizey+20)
        #rect = QRectF(0,0,1000,1000)
        return rect

    # paint with a big, wide colored line for now.  Rounded ends and stuff
    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        my_pen = QPen(self.color, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin);
        my_pen.setWidth(5)
        painter.setPen(my_pen)
        painter.setBrush(Qt.NoBrush);
        path = QPainterPath()  
        #path.moveTo(self.sourcePoint)
        #path.lineTo(self.destinationPoint); 
        # lookup the output port position by using the object name to index to the object type, then look in outputOffsets
        startx = self.sourceObject.pos().x()+outputOffsets[operationsType[self.sourceObject.objectName()]][0]
        starty = self.sourceObject.pos().y()+outputOffsets[operationsType[self.sourceObject.objectName()]][1]
        # lookup the input port position by converting object name to type and looking in inputOffsets
        endx = self.destinationObject.pos().x() + inputOffsets[operationsType[self.destinationObject.objectName()]][0]
        endy = self.destinationObject.pos().y() + inputOffsets[operationsType[self.destinationObject.objectName()]][1]
        path.moveTo(QPointF(startx,starty));
        path.lineTo(QPointF(endx,endy));
        #self.path.cubicTo(cp1.x(),cp1.y(),cp2.x(),cp2.y(),destPoint.x(),destPoint.y()); 
        painter.drawPath(path);    
        
    def advance(self):
        self.prepareGeometryChange()
        self.update(self.boundingRect())
      
    
#------------------------------------------------------------------------------------------------
# This class, the WorkspaceManager, handles the logic of adding and connecting workspace steps. 
# A list of steps and connecting edges, along with the dynamic objects names, is maintained and
# this class manages the QML display of the workspace itself.  
#------------------------------------------------------------------------------------------------

class workflowManager(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        #self._numNodes = 0
        self._numOperations = 0
        self._operations = []
        # operations type is a dictionary with names as keys and types as values {'operation_0' : 'DataIntegrator'}
        self._operationsType = {}
        self._edges = []
        self._numEdges = 0
        self._currentEdge = 0
        self.newalgorithm = ""
        self._savedViewObject = ""

  
     #--------------------------------------------------------------------------------
      # this is the slot that is called from Qt when a new algorithm needs to be created. This
      # method is directly callable because it is a slot and it belongs to the context property 
      # which is this object.
      
    @QtCore.pyqtSlot(str)
    def slot_add_algorithm(self, str):
        print "adding algorithm: ", str
        # find the location to add the new object at by subtracting the corner of the
        # workspace from the current cursor position (to find the offset into the workspace
        # at which to drop the new instance
        currentPosition = QCursor.pos()
        print "current= ",currentPosition
        
        # this doesn't change the coordinates.  Unity transform
        #pointMappedToScene = self._workspaceObject.mapFromScene(QPointF(currentPosition))
        #print "mapped to scene= ",pointMappedToScene
        #windowroot = self._savedViewObject.rootObject()
        #mappedPoint = self._workspaceObject.mapFromItem(windowroot,QPointF(currentPosition))
        #print "mapped= ",mappedPoint
        #print "tl= ",topLeftWorkspaceCorner
        #relativeOffset.pos(currentPosition.pos() - topLeftWorkspaceCorner
        
        # create a visual representation of the algorithm
        self._addAlgorithm(str,self._numOperations,currentPosition.x(),currentPosition.y())

        # increment the operation count
        self._numOperations += 1

    
    # This property "newalgorithm" will belong to the workflowManager object on 
    # the QML side.  it can be set and read because we are attaching handlers to it.
    
    def _set_newalgorithm(self,newalg):
        self.newalgorithm = newalg
        self.on_newalgorithm.emit()
 
    def _get_newalgorithm(self,newalg):
        return self.newalgorithm
    
    # declare a signal that is fired off when the property value is changed
    on_newalgorithm = QtCore.pyqtSignal()
        
    # set the getter and setter to call when this property value changes    
    #newalgorithm = QtCore.property(str, _get_newalgorithm,
    #                                   _set_newalgorithm, 
    #                                   notify=on_newalgorithm)


    #--------------------------------------------------------------------------------
    # define a method that discovers the workspace entry in the application UI's
    # scene graph and saves the reference to it.  A persistent reference is kept to 
    # ease setting the parent pointers of objects added dynamically to the QDeclarativeScene
    #---------------------------------------------------------------------------------
    def findAndSaveWorkspaceFromRoot(self,rootObject):
        objects = []
        objects = rootObject.findChildren(QtGui.QGraphicsObject,"workspace")
        print "found children count: ", len(objects)
        self._workspaceObject =  objects[0]        
        print "child's name is: ",objects[0].objectName()


    #--------------------------------------------------------------------------------
    # define a method that saves the Declarative View object
    #--------------------------------------------------------------------------------    
    def saveViewObject(self, viewObject):
        self._savedViewObject =  viewObject    
        return self._savedViewObject    


    #--------------------------------------------------------------------------------
    # this internal method is called whenever the user drops a new algorithm into the workspace 
    # and it needs to be instantiated and added to the workflow being built through the UI.
    # This private method is the "logic" called when the slot "slot_add_algorithm" is invoked 
    # by the UI.  This method adds a new element to the workflow and updates the internal
    # lists of algorithms in the workflow.   
    #-------------------------------------------------------------------------------- 
    def _addAlgorithm(self,name,operationNumber,xpos,ypos):
        print "python local method adding: ",name, " at location (",xpos,",",ypos,")"
        engine = self._savedViewObject.engine()
        print "engine: ", engine
        newalgo_comp = QtDeclarative.QDeclarativeComponent(engine)
          
        for case in switch(name):
           if case("Lagrange"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/Lagrange.qml"));
            break;
           if case("OpenModeller"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/OpenModeller.qml"));
            break;
           if case("DataIntegrator"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/DataIntegrator.qml"));
            break;
           if case("FitContinuous"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/FitContinuous.qml"));
            break;
           if case("FitDiscrete"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/FitDiscrete.qml"));
            break;
           if case("TreeFromFile"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/TreeFromFile.qml"));
            break;
           if case("OpenTreeOfLife"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/OpenTreeOfLife.qml"));
            break;
           if case("CharacterMatrix"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/CharacterMatrix.qml"));
            break;
           if case("TreeTransform"):
            newalgo_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/operations/TreeTransform.qml"));
            break;

           if case():
              document.write("Sorry, we are out of " + name + ".<br>");
                  
        # instantiate the component to create a new instance
        newalgo_item = newalgo_comp.create()
        # assign a unique object name to the workstep instance
        newalgo_item.setObjectName("operation_"+str(operationNumber))
        # store the algorithm in the list of operations saved by the workflow manager.  The type of the operation
        # is stored in a parallel list so we can reference this to find pixel offsets later depending on the
        # type of the operation
        self._operations.append(newalgo_item)
        # build a dictionary indexed by object name that returns the object type.  Keeping local and global one just 
        # because the Segment class needs access to this cross reference, as well. 
        self._operationsType[newalgo_item.objectName()] = name
        operationsType[newalgo_item.objectName()] = name
        #print "newalgo_item=", newalgo_item
        print "new objname is: ",newalgo_item.objectName()
        # set the visual position of the icon and add it to the visual scene so it displays. The 
        # position it is added to the scene needs to be fixed, but this doesn't affect operation, just
        # aesthetics.  We need to translate from screen to workspace rectangle coordinates to get it right. 
        newalgo_item.setPos(float(xpos),float(ypos))
        self._savedViewObject.scene().addItem(newalgo_item)
        newalgo_item.setParentItem(self._workspaceObject)


	#-------------------------------------------------------------------------------------
    # Slot to add an outgoing edge on the the output of a workstep declaration. 
    # the user clicks on the output port and this edge appears.  A QGraphicsObject is 
    # passed as an argument, so we have the source that initiated the edge and we can 
    # use this to keep them together as the souce object is moved around.  
	#-------------------------------------------------------------------------------------    
    @QtCore.pyqtSlot(QGraphicsObject,str)
    def addEdgeFromWorkstep(self,workstep_source_object,workstepname):
        print "adding edge from workstep named: ",workstepname
        #workstep_source_object_list = self._workspaceObject.findChildren(QtGui.QGraphicsObject,workstepname)
        #workstep_source_object = workstep_source_object_list[0]
        print "source workstep discovered objectname is: ",workstep_source_object.objectName()
  
            # create an endpoint object for the unattached end of the segment
        engine = self._savedViewObject.engine()
        print "engine: ", engine
        newcomp = QtDeclarative.QDeclarativeComponent(engine)
        newendpoint_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/GraphNode.qml"));
        newendpoint_item = newendpoint_comp.create()
        # set a name and set the index value so we know which edge we are dealing with
        newendpoint_item.setObjectName("endpoint"+str(self._numEdges))
        newendpoint_item.setProperty("edgeNumber",self._numEdges)
        self._savedViewObject.scene().addItem(newendpoint_item)
        newendpoint_item.setParentItem(self._workspaceObject)
        
        # fill in an entry in the name to type dictionary so we can look up offsets for edges during rendering
        self._operationsType[newendpoint_item.objectName()] = 'endpoint'
        operationsType[newendpoint_item.objectName()] = 'endpoint'      
          
        # find an endpoint off to the right of the source workstep and arbitrary amount.  We will drag this endpoint
        # to connect it to another workstep later
        sourcepoint = workstep_source_object.pos()
        newendpoint_item.setPos(QPointF(sourcepoint.x()+350,sourcepoint.y()+200))

        # color could be derived from the type of object we are reading the output from
        color = QColor(100,0,100)
        newedge_item = Segment(color,self._workspaceObject)

        # assign a unique object name to the edge and assign the source and destination 
        # objects so the edge can follow the movement of the worksteps
        newedge_item.setObjectName("edge"+str(self._numEdges))
        newedge_item.setSourceObject(workstep_source_object)
        newedge_item.setDestinationObject(newendpoint_item)
            
        # store the edge in the list of edges saved by the workflow manager
        self._edges.append(newedge_item)
        self._numEdges = self._numEdges+1
        print "new edge name is: ",newedge_item.objectName()

	#-------------------------------------------------------------------------------------
    # Slot to add an outgoing edge on the the output of a workstep declaration. 
    # the user clicks on the output port and this edge appears.  A QGraphicsObject is 
    # passed as an argument, so we have the source that initiated the edge and we can 
    # use this to keep them together as the souce object is moved around.  
	#-------------------------------------------------------------------------------------    
    @QtCore.pyqtSlot(QGraphicsObject,str)
    def addQMLEdgeFromWorkstep(self,workstep_source_object,workstepname):
        print "adding QML edge from workstep named: ",workstepname
        #workstep_source_object_list = self._workspaceObject.findChildren(QtGui.QGraphicsObject,workstepname)
        #workstep_source_object = workstep_source_object_list[0]
        print "source workstep discovered objectname is: ",workstep_source_object.objectName()
  
            # create an endpoint object for the unattached end of the segment
        engine = self._savedViewObject.engine()
        print "engine: ", engine
        newcomp = QtDeclarative.QDeclarativeComponent(engine)
        newendpoint_comp = QtDeclarative.QDeclarativeComponent(engine,QUrl.fromLocalFile("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt/Declarations/GraphEdge.qml"));
        newendpoint_item = newendpoint_comp.create()
        # set a name and set the index value so we know which edge we are dealing with
        newendpoint_item.setObjectName("endpoint"+str(self._numEdges))
        newendpoint_item.setProperty("edgeNumber",self._numEdges)
        self._savedViewObject.scene().addItem(newendpoint_item)
        newendpoint_item.setParentItem(self._workspaceObject)
        
        # fill in an entry in the name to type dictionary so we can look up offsets for edges during rendering
        self._operationsType[newendpoint_item.objectName()] = 'endpoint'
        operationsType[newendpoint_item.objectName()] = 'endpoint'      
          
        # find an endpoint off to the right of the source workstep and arbitrary amount.  We will drag this endpoint
        # to connect it to another workstep later
        sourcepoint = workstep_source_object.pos()
        newendpoint_item.setPos(QPointF(sourcepoint.x()+350,sourcepoint.y()+200))

        # color could be derived from the type of object we are reading the output from
        color = QColor(100,0,100)
        newedge_item = Segment(color,self._workspaceObject)

        # assign a unique object name to the edge and assign the source and destination 
        # objects so the edge can follow the movement of the worksteps
        newedge_item.setObjectName("edge"+str(self._numEdges))
        newedge_item.setSourceObject(workstep_source_object)
        newedge_item.setDestinationObject(newendpoint_item)
            
        # store the edge in the list of edges saved by the workflow manager
        self._edges.append(newedge_item)
        self._numEdges = self._numEdges+1
        print "new edge name is: ",newedge_item.objectName()



	#----------------------------------------------------------------------------------
	# Slot that is called by the QML objects when they are moved.  This is necessary to 
	# force re-rendering of the edges since the QGraphicsItems don't really know when 
	# to refresh themselves the way they have been implemented in the Segment class.
	#----------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def updateAllEdges(self):
        #print "updating"
        for i in range(self._numEdges):
            self._edges[i].update(0,0,1600,1400)
  
 	#----------------------------------------------------------------------------------
	# Slot that is called by the QML objects when they are moved.  This is necessary to 
	# force re-rendering of the edges since the QGraphicsItems don't really know when 
	# to refresh themselves the way they have been implemented in the Segment class.
	#----------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def updateAllOperations(self):
        #print "updating"
        for i in range(self._numOperations):
            self._operations[i].update(0,0,1600,1400)
  

  
	#-------------------------------------------------------------------------------------
    # Slot to add an edge as the input to a nearby workstep.  A screen space search
    # is conducted to find a workstep nearby (with radius of 100 pixels) and  
	#-------------------------------------------------------------------------------------    
    @QtCore.pyqtSlot(QGraphicsObject,str)
    def addEdgeInputToWorkstep(self,edge_object,workstepname):
    	print "adding workstep input to edge named: ",workstepname
    	# look through the operations to find one close to the drop location
    	for i in range(self._numOperations):
    		operation_posx = self._operations[i].pos().x()
    		operation_posy = self._operations[i].pos().y()
    		distanceToWorkstep = abs(edge_object.pos().x()-operation_posx)*abs(edge_object.pos().x()-operation_posx) + abs(edge_object.pos().y()-operation_posy)*abs(edge_object.pos().y()-operation_posy)
    		print "distance to ",self._operations[i].objectName(), " is ",distanceToWorkstep
    		# TODO: fix test against top left corner of workstep.  It should be looking for input connectors instead
    		if (distanceToWorkstep < 150*150):
				# we found the close workstep, so make it the new destination object and delete the dot
				thisEdgeNumber = edge_object.property("edgeNumber").toInt()[0]
				print "connecting operation ",self._operations[i].objectName(), " to edge: ",thisEdgeNumber
				print "this operation is of type: ", operationsType[self._operations[i].objectName()]
				self._edges[thisEdgeNumber].setDestinationObject(self._operations[i])
				# force rerender around the destination object
				self._operations[i].update(0,0,1000,1000)
				# removing the object crashes the app for some reason, just make it invisible
				#self._savedViewObject.scene().removeItem(edge_object)
				edge_object.setProperty("opacity",0.0)
				self.updateAllEdges()