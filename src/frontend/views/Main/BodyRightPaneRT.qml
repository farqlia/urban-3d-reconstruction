import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants
import Components

Rectangle {
    id: bodyRightPaneRT
    color: ColorConst.primaryColor

    Border_ {
        anchors.fill: parent

        ColumnLayout {
            anchors.fill: parent

            LayoutItemProxy {
                target: buttonSplat3DMode
                width: RoundButtonConst.renderingModeRadius
                height: RoundButtonConst.renderingModeRadius
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: FormatConst.smallMargin
            }

            Rectangle {
                Layout.fillWidth: true
                height: FormatConst.defaultBorderWeight
                color: ColorConst.secondaryColor
            }

            LayoutItemProxy {
                target: buttonCategorization3DMode
                width: RoundButtonConst.renderingModeRadius
                height: RoundButtonConst.renderingModeRadius
                Layout.alignment: Qt.AlignHCenter
                Layout.bottomMargin: FormatConst.smallMargin
            }
        }
    }

    RoundButton_ {
        id: buttonSplat3DMode
        icon.source: "../icons/3d-cube.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
    RoundButton_ {
        id: buttonCategorization3DMode
        icon.source: "../icons/categorization.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
}