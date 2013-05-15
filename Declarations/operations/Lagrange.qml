import Qt 4.7

Rectangle {
        	id: vizitem
        	width: 70
        	height: 90
 
        
        Image {
            x: -5; y: -5
            width: 80; height: 100
            source: "../../images/nodes/lagrange.png"
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
			}
		}
        	
        Text {
        	id: operationname
            text: "Lagrange"
            x: 25; y: 45
            font.family: "Helvetica"
            font.pointSize: 24
            opacity: 0.0
        }
}