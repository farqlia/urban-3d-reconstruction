import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants
import Components

Rectangle {
    id: bodyRightPaneRB
    color: ColorConst.primaryColor

    Border_ {
        anchors.fill: parent

        RowLayout {
            anchors.fill: parent
            anchors.margins: FormatConst.defaultPadding

            LayoutItemProxy {
                target: buttonMoveAction
                width: RoundButtonConst.renderingModeRadius
                height: RoundButtonConst.renderingModeRadius
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
            }

            LayoutItemProxy {
                target: buttonRotateAction
                width: RoundButtonConst.renderingModeRadius
                height: RoundButtonConst.renderingModeRadius
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            LayoutItemProxy {
                target: buttonZoomAction
                width: RoundButtonConst.renderingModeRadius
                height: RoundButtonConst.renderingModeRadius
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            }
        }
    }

    RoundButton_ {
        id: buttonMoveAction
        icon.source: "../icons/palm-of-hand.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
    RoundButton_ {
        id: buttonRotateAction
        icon.source: "../icons/360.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
    RoundButton_ {
        id: buttonZoomAction
        icon.source: "../icons/magnifier.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
}