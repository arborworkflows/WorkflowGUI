import Qt 4.7

Rectangle {
    width: 900
    height: 900

    ListModel {
        id: vizmodel
        ListElement { name: "TwoVariable"; pict: "../images/views/viz1.png"}
        ListElement { name: "GlobalGeoView"; pict: "../images/views/viz2.png"}
        ListElement { name: "NetworkScatter"; pict: "../images/views/viz3.png"}
        ListElement { name: "HeatMap"; pict: "../images/views/viz4.png"}
        ListElement { name: "Taxonomy"; pict: "../images/views/viz5.png"}
        ListElement { name: "LatLongGeo"; pict: "../images/views/viz6.png"}
        ListElement { name: "ConicalGeo"; pict: "../images/views/viz7.png"}
        ListElement { name: "TreeView"; pict: "../images/views/viz8.png"}
        ListElement { name: "ElevationView"; pict: "../images/views/viz9.png"}
    }

    Image {
        anchors.fill: parent
        source: "../images/Fabric-seamless.jpg"
        opacity:  0.2
    }

    Component {
        id: vizdelegate
        Column {
            width: grid.cellWidth; height: grid.cellHeight
        Image {
            width: 60; height: 60
            source: pict
        }
        Text {
            text: name
            y: 80
        }
        }
    }


    GridView {
        model: vizmodel
        width: parent.width*0.35
        height: parent.height*0.8
        cellWidth: 120; cellHeight: 100
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 50
        delegate: vizdelegate

    }
}
