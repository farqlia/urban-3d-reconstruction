import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants

Border {
    id: tab

    property var model: []
    property Item placeholder: null
    
    onPlaceholderChanged: {
        if (placeholder) {
            placeholder.parent = placeholderContainer
        }
    }

    onModelChanged: {
        listView.model = model
    }

    color: "transparent"
    border.color: "transparent"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: FormatConst.defaultMargin

        Item {
            id: placeholderContainer
            Layout.fillWidth: true
        }

        ListView {
            id: listView
            Layout.alignment: Qt.AlignHCenter
            Layout.fillHeight: true
            Layout.fillWidth: true
            model: tab.model
            spacing: FormatConst.smallPadding

            delegate: ListEntry {
                text: modelData
            }
        }
    }
}