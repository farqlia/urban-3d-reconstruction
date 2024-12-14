import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants
import Components

Rectangle {
    id: footer
    color: ColorConst.primaryColor

    RowLayout {
        anchors.fill: parent

        LayoutItemProxy {
            target: textLicense
            Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
        }

        Spacer_ {}

        LayoutItemProxy {
            target: textBuildVersion
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
        }
    }
    Text {
        id: textLicense
        text: "AGPL-3.0 license"
        color: ColorConst.secondaryColor
    }
    Text {
        id: textBuildVersion
        text: "version: 0.0.1-alpha-build"
        color: ColorConst.secondaryColor
        font.pointSize: 12
    }
}