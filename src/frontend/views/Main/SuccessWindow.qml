
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Components
import Constants

Rectangle {
    id: successWindow
    color: ColorConst.primaryColor

    width: FormatConst.popupWidth
    height: FormatConst.popupHeight

    Border_ {
        width: parent.width
        height: parent.height

        ColumnLayout {
            anchors.fill: parent

            RoundButton_ {
                icon.source: "../icons/ok.png"
                icon.width: RoundButtonConst.headerImageRadius
                icon.height: RoundButtonConst.headerImageRadius
                icon.color: buttonRun.hovered? ColorConst.hoverColor : ColorConst.secondaryColor
                Layout.alignment: Qt.AlignHCenter
            }

            Text {
                text: ""
                color: ColorConst.secondaryColor
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                onClicked: {
                    isBuildSucc.data = false
                }
                background: Rectangle {
                    color: ColorConst.secondaryColor
                    radius: FormatConst.defaultRadius
                }
                contentItem: Text {
                    text: "Close"
                    color: ColorConst.primaryColor
                    font.bold: true
                    anchors.centerIn: parent
                    font.pointSize: FormatConst.smallFontSize
                }
                padding: FormatConst.defaultPadding
            }
        }
    }
}