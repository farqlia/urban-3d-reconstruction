import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants
import Components

Rectangle {
    id: bodyRightPaneRB
    color: ColorConst.primaryColor

    RowLayout {
        anchors.fill: parent

        LayoutItemProxy {
            target: buttonMoveAction
            width: RoundButtonConst.renderingModeRadius
            height: RoundButtonConst.renderingModeRadius
            Layout.alignment: Qt.AlignBottom
        }

        LayoutItemProxy {
            target: buttonRotateAction
            width: RoundButtonConst.renderingModeRadius
            height: RoundButtonConst.renderingModeRadius
            Layout.alignment: Qt.AlignBottom
        }

        LayoutItemProxy {
            target: buttonZoomAction
            width: RoundButtonConst.renderingModeRadius
            height: RoundButtonConst.renderingModeRadius
            Layout.alignment: Qt.AlignBottom
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