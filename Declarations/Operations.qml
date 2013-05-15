import Qt 4.7


// the operations panel which contains algorithm steps that can be added into workflows
Rectangle {
    width: 250
    height: 500

	// this list model defines all the algorithms that are in the list.  TODO: this should
	// be loaded from an XML or JSON file eventually or have active management by the workflowManager, etc.
	
    ListModel {
        id:  datamodel
        ListElement { name: "DataIntegrator"; pict: "../images/operations/DataIntegrator.png"}
        ListElement { name: "OpenModeller"; pict: "../images/operations/OpenModeller.png"}
        ListElement { name: "FitContinuous"; pict: "../images/operations/FitContinuous.png"}
        ListElement { name: "FitDiscrete"; pict: "../images/operations/FitDiscrete.png"}
        ListElement { name: "TreeTransform"; pict: "../images/operations/TreeTransform.png"}
        ListElement { name: "Lagrange"; pict: "../images/operations/Lagrange.png"}
        ListElement { name: "dataoutput"; pict: "../images/operations/dataoutput.png"}
    }

	// background image for the panel
    Image {
        anchors.fill: parent
        source: "../images/Fabric-seamless.jpg"
        opacity:  0.2
    }

	// this is the delegate used to draw each operation.  It has a containing Item{}, the 
	// highest graphical level for the object.  There is an image and text as well.  When the 
	// user drags the icon off of the "stack of operations", the Item is dragged until dropped
	// onto the workspace.  At this point, we reset the drag coordinates to zero (setting vizitem.x 
	// and vizitem.y = 0) and create a new icon owned by the workspace and make the corresponding
	// change to the underlying workflow data structures as well. 
	
    Component {
        id: vizdelegate

        Item {
        	id: vizitem
        	width: 130
        	height: 150
        Image {
            width: 120; height: 140
            source: pict
            id: delegateimage
            
            MouseArea {
         		anchors.fill: parent
         		drag.target: parent.parent
         		drag.axis: Drag.XandYAxis
         		hoverEnabled: true
         		onPressed: {}
				onReleased: {
						// get unique name for task.  This property name is queried from
						// the logic side to find out what operation was "dropped in" 
						//workflowmgr.newalgorithm = name
						// call logic to add the new operation
						workflowmgr.slot_add_algorithm(name)
						
						// reset the item (which was dragged from the operations list) 
						// back to where it belongs.  The index value is used to reset the
						// item because it is managed by a list view and needs to go back to 
						// the correct place on the list.  This is temporarily defeated, as we are
						// using the orignal icons for now, avoiding the QML component creation bug in
						// PySide.  
						
						vizitem.x = 0
						vizitem.y = index*vizitem.height
						}
				onEntered: {
					// TODO: use animation to make it cool.  Define states for the icon. We
					// will likely need to do states later anyway for highlighting connectors
					operationname.opacity = 1.0
					vizitem.opacity = 0.5
				}
				onExited: {
					operationname.opacity = 0.0
					vizitem.opacity = 1.0
				}
			}
		}
        	
        Text {
        	id: operationname
            text: name
            x: 25; y: 45
            font.family: "Helvetica"
            font.pointSize: 24
            opacity: 0.0
        }
    	}
    }


    ListView {
        model: datamodel
        width: 120
        orientation: ListView.Vertical
        height: parent.height*0.8
        anchors.centerIn: parent
        delegate: vizdelegate
    }

}
