import Qt 4.7

Rectangle {
    width: 1400
    height: 900

//    Text {
//        anchors.horizontalCenter: parent.horizontalCenter
//        anchors.top: parent.top
//        anchors.topMargin: 20
//        text: "Workspace"
//        font.pixelSize: 18
//    }


     Rectangle {
         objectName: "background"
         anchors.fill: parent
         gradient: Gradient {
 
             GradientStop { position: 0.0; color: "darkgreen" }
             GradientStop { position: 1.0; color: "#202020"}
 
         }
     }

//    Image {
//        x: 500; y: 200
//        source: "../images/operations/single-filter.png"
//        opacity:  1
//    }

//    Image {
//          x: 500; y: 320
//        source: "../images/operations/two-input-filter.png"
//        opacity:  1
//    }
}
