import QtQuick 1.0

/* read declarations from qml directory */

import "Declarations"

Rectangle {
	objectName: "rootObject"
    width: 1000
    height: 850

 // operation panel where workflow steps are declared.  Steps can be dropped from here
 // into the workspace
 Operations {
	x: parent.width-250; y:0; z: 1
	width: parent*0.2; height: parent.height
    }
    
  // this is the definition of the place where workflow steps are dropped and 
  // hooked together  
  Workspace {
  	objectName: "workspace"
  	x: parent*0.2
  }
  
  // panel on the left with objects we can drag in that are data sources
 Datapanel {
	x: 0; y:0
	width: parent*0.2; 
	height: parent.height
  }

}    