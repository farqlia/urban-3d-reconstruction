
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Constants

Popup {
    id: popup
    modal: true
    focus: true
    anchors.centerIn: parent

    closePolicy: Popup.NoAutoClose

    property string text: ""

    contentItem: Border {
        width: parent.width
        height: parent.height

        ColumnLayout {
            anchors.fill: parent

            Image {
                source: "../icons/ok.png"
                Layout.preferredWidth: 50
                Layout.preferredHeight: 50
                Layout.alignment: Qt.AlignHCenter
            }

            Text {
                text: popup.text
                color: ColorConst.secondaryColor
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            Button {
                Layout.alignment: At.AlignHCenter
                onClicked: popup.close()
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