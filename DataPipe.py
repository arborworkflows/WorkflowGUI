#
#  class to represent data connections between workflow steps
#  KnowledgeVis 2013
#

import math
import random
import sys
from PyQt4.QtCore import (QObject, QPointF, QRectF, QTimer, Qt, SIGNAL,
        SLOT)
from PyQt4.QtGui import (QApplication, QBrush, QColor, QDialog, QColor,
        QGraphicsItem, QGraphicsScene, QGraphicsView, QHBoxLayout,
        QPainter, QPainterPath, QPolygonF, QPushButton, QSlider,
        QVBoxLayout)
        
from PyQt4 import QtDeclarative
               
class DataPipe(QtDeclarative.QDeclarativeItem):

    def __init__(self, color):
        super(DataPipe, self).__init__()
        self.color = color
        self.sourcePoint = QPoint(0,0,0)
        self.destinationPoint = QPoint(0,0,0)
        self.rect = QRectF(0, -20, 30, 40)
        self.path = QPainterPath()
        self.change = 1
        self.angle = 0

    def setSourcePoint(self,srcp):
        self.sourcePoint = srcp

    def setDestinationPoint(self,dstp):
        self.destinationPoint = dstp

    def boundingRect(self):
        return self.path.boundingRect()

    def shape(self):
        return self.path

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(QColor(0,0,0)))
        painter.setBrush(QBrush(self.color))
        painter.pen().setWidth(4);
        painter.setBrush(Qt.NoBrush);
        painter.drawPath(self.path);
        
        self.path.moveTo(sourcePoint);
        self.path.lineTo(self.destinationPoint);
        #self.path.cubicTo(cp1.x(),cp1.y(),cp2.x(),cp2.y(),destPoint.x(),destPoint.y()); 
        painter.drawPath(self.path);    

    def advance(self, phase):
        if phase == 0:
            matrix = self.matrix()
            matrix.reset()
            self.setMatrix(matrix)
            self.angle += self.change * random.random()
            if self.angle > 4.5:
                self.change = -1
                self.angle -= 0.00001
            elif self.angle < -4.5:
                self.change = 1
                self.angle += 0.00001
        elif phase == 1:
            self.rotate(self.angle)