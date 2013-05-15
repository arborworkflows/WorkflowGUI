import QtQuick 1.1

Item {
        	id: vizitem
        	width: 120
        	height: 230
        	
        	// we could put the port definitions here and look for them in the code, but 
        	// I had trouble with this initially, so went away from this toward a single
        	// global lookup table.  This method could be used though, with setProperty() and
        	// property() calls 
        	
        	property int outputOffsetX:  150
        	property int outputOffsetY:  127
         
        Image {
            x: -5; y: -5
            width: 150; height: 250
            source: "../../images/operations/DataIntegrator.png"
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
					//operationname.opacity = 1.0
				}
				onExited: {
					//operationname.opacity = 0.0
				}
				
				// this forced update is needed to force re-render of the data pipes that connect
				// the worksteps, since they are implemented as QPainter classes.  Maybe there
				// is something missing in the Segment class.  
				
				onPositionChanged: {
                    workflowmgr.updateAllEdges()
              }
 
			}
		}

   // an input connector
        Rectangle {
            id: inputrect
            x: 0; y:55
            width: 30; height: 25
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
            x: 100; y:110
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
            text: "Data Integrator"
            x: 25; y: 45
            font.family: "Helvetica"
            font.pointSize: 24
            opacity: 0.0
        }
}