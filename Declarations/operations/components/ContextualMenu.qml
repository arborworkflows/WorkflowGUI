import QtQuick 1.0

import "ContextualMenu.js" as CtxMenu

Rectangle {
    id: menuRoot

    property ListModel model
    property int itemFontSize : 15

    signal itemClicked(int index)

    opacity: 0
    anchors.fill: parent
    color: "#80000000"

    // intercepts clicks outside the menu area, that hide the menu itself
    MouseArea {
	anchors.fill: parent
	onClicked: CtxMenu.hideMenu()
    }

    // intercepts press-and-hold interactions on the menu parent, that show the menu itself
    MouseArea {
	id: menuMouseArea
	anchors.fill: parent
	onPressAndHold: CtxMenu.showMenu(mouse)
    }

    Rectangle {
	id: menu

	color: "#336699"

	width: CtxMenu.getMenuWidth() + 1
	height: CtxMenu.getMenuHeight()

	ListView {
	    id: menuList

	    clip: true
	    model: menuRoot.model
	    anchors.fill: parent

	    delegate: Rectangle {
		id: listViewItem
		color: (activeFocus ? "lightsteelblue" : "transparent")
		border {width: 1;color: "black"}
		width: menu.width - 1
		height: itemText.height
		Text {
		    id: itemText
		    text: name
		    width: listViewItem.width
		    font.pointSize: itemFontSize
		    elide: Text.ElideRight
		}
		MouseArea {
		    anchors.fill: parent
		    onClicked: {
			itemClicked(index);
			CtxMenu.hideMenu();
		    }
		}
		Keys.onReturnPressed: {
		    itemClicked(index);
		    CtxMenu.hideMenu();
		}
	    }
	}
    }

    states: State {
	name: "visible"
	PropertyChanges {target: menuRoot; opacity: 1}
    }

    transitions: Transition {
	NumberAnimation {
	    target:  menuRoot
	    properties: "opacity"
	    duration: 250
	}
    }
    Component.onCompleted: CtxMenu.initializeMenu()
}
