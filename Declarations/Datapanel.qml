import Qt 4.7

Rectangle {
    width: 250
    height: 500

    ListModel {
        id:  datamodel
        ListElement { name: "OpenTreeOfLife"; pict: "../images/operations/OpenTreeOfLife.png"}
        ListElement { name: "LifeMapper"; pict: "../images/operations/LifeMapper.png"}
        ListElement { name: "TreeFromFile"; pict: "../images/operations/TreeFromFile.png"}
        ListElement { name: "CharacterMatrix"; pict: "../images/operations/CharacterMatrix.png"}
    }

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
        	width: 160
        	height: 140
        Image {
            width: 150; height: 100
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

