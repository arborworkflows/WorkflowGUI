import QtQuick 1.1

import "components"

// use an item because they are invisible, so there is no border around the picture

Item {
        	id: vizitem
        	width: 180
        	height: 200

        
        Image {
            x: -5; y: -5
            width: 180; height: 200
            source: "../../images/operations/FitContinuous.png"
            id: delegateimage
            opacity: 1.0
            
            MouseArea {
         		anchors.fill: parent
         		drag.target: parent.parent
         		drag.axis: Drag.XandYAxis
         		hoverEnabled: true
         		onPressed: {}
				onReleased: {}
				onEntered: {
					// TODO: use animation to make it cool.  Define states for the icon. We
					// will likely need to do states later anyway for highlighting connectors
					operationname.opacity = 1.0
				}
				onExited: {
					operationname.opacity = 0.0
				}
				// this forced update is needed to force re-render of the data pipes that connect
				// the worksteps, since they are implemented as QPainter classes.  Maybe there
				// is something missing in the Segment class.  
				
				onPositionChanged: {
				    workflowmgr.updateAllOperations()
                    workflowmgr.updateAllEdges()

              }
			}
			
			// This is a pop up menu that happens if we long click over the options button
			// It is inside an "Item" to restrict its mouse stealing to the subregion immediately
			// around the options button
			
			Item {
			  x: 50; y: 140
			  width: 100; height: 40
			  
                ContextualMenu {
                    onItemClicked: console.log("clicked item: " + index)

                    model: ListModel {
                        ListElement {name: "Brownian"}
                        ListElement {name: "O-U"}
                        ListElement {name: "Early Burst"}
                    }
                }
            }
			
		}
		
	    // an input connector
        Rectangle {
            id: inputrect
            x: 0; y:85
            width: 40; height: 35
            opacity: 0.2
            
            MouseArea {
              anchors.fill: parent
              preventStealing: true
              hoverEnabled: true
              onEntered: {
                inputrect.opacity = 0.5
                inputrect.color = "red"
             
              }
              onExited:  {
                inputrect.color = "white"
                inputrect.opacity = 0.2
                
              }
  
            }
        }
		
	    // an output connector
        Rectangle {
            id: outputrect
            x: 130; y:85
            width: 50; height: 35
            opacity: 0.2
            
            MouseArea {
              anchors.fill: parent
              preventStealing: true
              hoverEnabled: true
              onEntered: {
                outputrect.opacity = 0.5
                outputrect.color = "red"
              }
              onExited:  {
                outputrect.color = "white"
                outputrect.opacity = 0.2
                
              }
  
              onPressed: {
                // start an output pipe. We are passing the id of the "vizitem" here
                // so that the slot can attach the edge to the position of this 
                // object and have it updated automatically
                workflowmgr.addEdgeFromWorkstep(vizitem,parent.parent.objectName)
              }
            }
        }
        	
        Text {
        	id: operationname
            text: "Fit Continuous"
            x: 25; y: -20
            font.family: "Helvetica"
            font.pointSize: 24
            opacity: 0.0
        }
}