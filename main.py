

import os
import sys


from PyQt4.QtCore import (Qt, SIGNAL,QUrl)
from PyQt4.QtGui import (QApplication, QDialog, QHBoxLayout, QVBoxLayout,
        QListWidget, QListWidgetItem, QSplitter, QTableWidget, QPushButton,QGraphicsView)
from PyQt4 import QtDeclarative


import geigerWrap
import workflowManager
 
class Form(QDialog):
   
    # Define the main user interface
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.button = QPushButton("Run Geiger Script") 
        self.quitbutton = QPushButton("Quit")
        wf_manager = workflowManager.workflowManager()
		
        # change to directory where the code is stored, so we can reference the
        # qml directory using a relative pathname. 
        # TODO: pack files into Qt resources eventually instead of absolute pathnames
        os.chdir("/Users/clisle/Projects/Arbor/code/exploration/ArborUsingPyQt")
        self.mapview = QtDeclarative.QDeclarativeView()
        self.mapview.setSource(QUrl.fromLocalFile("arbor-ui.qml")) 
        self.mapview.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        
        self.mapview.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        
        # install the Python workflowManager definition as a property in the QML context
        # so it can be referenced in the context and slots of the class can be invoked through QML
        self.mapview.rootContext().setContextProperty('workflowmgr', wf_manager) 
        
        # as part of initialization, have the workflowMgr dig around in the QML hierarchy, 
        # discover the workflow and save a private handle to the workflow so we can manage
        # the workflow UI canvas from the logic side. 
        
        #save pointer to the view. It is needed to instantiate new objects
        wf_manager.saveViewObject(self.mapview)
   
        wf_manager.findAndSaveWorkspaceFromRoot(self.mapview.rootObject())
        
             
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.mapview)
        layout.addWidget(self.quitbutton)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)
        self.quitbutton.clicked.connect(self.quitprogram)

       
    # Initialize the Geiger module under R 
    def greetings(self):
        print ("Running Geiger Init...") 
        geigerWrap.gw_InitGeiger()
        print ("Finished Geiger Init...") 
               
    # Closeout any leftover processes and interfaces, then quit
    def quitprogram(self):
        print ("Safe Closeout...") 
        geigerWrap.gw_ShutdownGeiger()
        quit()

 
 
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    # the window opens up really tiny without this, because QML size wasn't set
    form.setMinimumSize(800,600)
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())