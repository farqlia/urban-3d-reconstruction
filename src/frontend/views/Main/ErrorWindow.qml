import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Constants
import Components

Rectangle {
    id: errorWindow
    color: ColorConst.primaryColor
    
    width: FormatConst.popupWidth
    height: FormatConst.popupHeight

    Border_ {
        width: parent.width
        height: parent.height

        ColumnLayout {
            anchors.fill: parent

            Image {
                source: "../icons/cancel.png"
                Layout.preferredWidth: 50
                Layout.preferredHeight: 50
                Layout.alignment: Qt.AlignHCenter
            }

            Text {
                text: buildInfo.data
                color: ColorConst.secondaryColor
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                onClicked: {
                    isBuildFail.data = false
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