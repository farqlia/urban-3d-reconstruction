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

    property real progressValue: 0.0
    property bool buildCanceled: false

    onProgressValueChanged: {
        progressBar.value = progressValue
    }

    contentItem: Border {
        width: parent.width
        height: parent.height

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
                value: progressValue
                padding: 2

                onValueChanged: {
                    if (value === 0) {
                        // Display Success Popup
                        popup.close()
                    }
                }

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
                onClicked: {
                    popup.buildCanceled = true
                    popup.close()
                }
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