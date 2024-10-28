import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Constants

Popup {
    id: popup
    modal: true
    focus: true
    anchors.centerIn: parent

    contentItem: Rectangle {
        width: parent.width
        height: parent.height
        color: ColorConst.primaryColor
        border.color: ColorConst.secondaryColor
        border.width: FormatConst.defaultBorderWeight
        radius: 10

        ColumnLayout {
            anchors.fill: parent

            AnimatedImage {
                Layout.preferredWidth: 50
                Layout.preferredHeight: 50
                Layout.alignment: Qt.AlignHCenter
                source: "../icons/loading.gif"
                cache: true
            }

            ProgressBar {
                id: progressBar
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                Layout.leftMargin: FormatConst.smallMargin
                Layout.rightMargin: FormatConst.smallMargin
                from: 0
                to: 100
                value: 50
                padding: 2

                background: Rectangle {
                    implicitWidth: parent.width
                    implicitHeight: 10
                    color: ColorConst.secondaryColor
                    radius: 10
                }

                contentItem: Item {
                    // implicitWidth: parent.width
                    // implicitHeight: 8

                    Rectangle {
                        width: progressBar.visualPosition * parent.width
                        height: parent.height
                        radius: 2
                        color: "#17a81a"
                        visible: !progressBar.indeterminate
                    }
                }
            }

            Button {
                Layout.alignment: Qt.AlignHCenter
                onClicked: popup.close()
                background: Rectangle {
                    color: ColorConst.secondaryColor
                    radius: 10
                }
                contentItem: Text {
                    text: "Cancel"
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