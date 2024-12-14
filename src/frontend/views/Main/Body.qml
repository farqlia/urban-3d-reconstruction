import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants
import Components

Rectangle {
    id: body
    color: ColorConst.primaryColor

    RowLayout {
        anchors.fill: parent
        // height: 900

        LayoutItemProxy {
            target: leftPane
            Layout.preferredWidth: 270
            Layout.fillHeight: true
            Layout.rightMargin: FormatConst.defaultMargin
        }

        LayoutItemProxy {
            target: rightPane
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
    BodyLeftPane_ {
        id: leftPane
    } 

    BodyRightPane_ {
        id: rightPane
    }
}