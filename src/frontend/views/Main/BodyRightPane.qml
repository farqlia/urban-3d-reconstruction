import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants
import Components

Rectangle {
    id: bodyRightPane
    color: ColorConst.primaryColor

    Border_{
        anchors.fill: parent

        GridLayout {
            id: rightMainLayout
            anchors.fill: parent
            columns: 2
            rows: 2

            CoordsTable_ {
                width: 300
                height: 70
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                Layout.topMargin: FormatConst.defaultMargin
                Layout.leftMargin: FormatConst.defaultMargin
            }

            Border_{
                width: 70
                height: 140
                Layout.alignment: Qt.AlignRight | Qt.AlignTop
                Layout.topMargin: FormatConst.defaultMargin
                Layout.rightMargin: FormatConst.defaultMargin

                ColumnLayout {
                    id: renderingModeLayout
                    anchors.fill: parent

                    LayoutItemProxy {
                        target: buttonSplat3DMode
                        width: RoundButtonConst.renderingModeRadius
                        height: RoundButtonConst.renderingModeRadius
                        Layout.alignment: Qt.AlignHCenter
                        Layout.topMargin: FormatConst.smallMargin
                    }

                    Rectangle {
                        width: parent.width
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

            Border_ {
                width: 200  
                height: 170
                Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                Layout.bottomMargin: FormatConst.defaultMargin
                Layout.leftMargin: FormatConst.defaultMargin
                // color: ColorConst.secondaryColor

                ColumnLayout {

                }
            }
            
            Border_ {
                width: 200
                height: 100
                Layout.alignment: Qt.AlignRight | Qt.AlignBottom
                Layout.bottomMargin: FormatConst.defaultMargin
                Layout.rightMargin: FormatConst.defaultMargin
                border.color: "transparent"

                RowLayout {
                    id: renderingActionLayout
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