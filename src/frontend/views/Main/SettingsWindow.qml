
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

import Components
import Constants
import "."

Rectangle {
    id: loadingWindow
    color: ColorConst.primaryColor

    width: FormatConst.popupSmallWidth
    height: FormatConst.popupHeight

    function getCopyVars() {
        var tempVars = [];
        for (var i = 0; i < settingsVars.data.length; i++) {
            tempVars.push(settingsVars.data[i]);
        }
        return tempVars;
    }

    function applyChanges() {
        for (var i = 0; i < listView.model.length; i++) {
            var item = listView.itemAtIndex(i).children[0].children[1];
            if (item) {
                var curr_model = listView.model[i];
                curr_model.input = item.text;
                listView.model[i] = curr_model;
            }
        }
        settingsVars.data = listView.model;
    }

    Border_ {
        width: parent.width
        height: parent.height

        ColumnLayout {
            anchors.fill: parent


            ListView {
                id: listView
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignHCenter
                Layout.margins: FormatConst.defaultMargin
                //spacing: FormatConst.smallPadding
                model: [1]
                //model: settingsVars ? getCopyVars() : []

                delegate: Item {
                    width: listView.width
                    height: content.height + FormatConst.smallPadding

                    RowLayout {
                        id: content
                       // anchors.fill: parent
                        spacing: FormatConst.smallPadding
                        anchors.horizontalCenter: parent.horizontalCenter

                        Text {
                            text: "COLMAP reconstruction  "
                            Layout.alignment: Qt.AlignCenter
                            color: ColorConst.secondaryColor
                            font.pointSize: FormatConst.smallFontSize
                            font.bold: true
                        }
                        Button {
                            id: loadReconstructionButton
                            font.pointSize: FormatConst.defaultFontSize
                            font.bold: true
                            background: Rectangle {
                                color: loadReconstructionButton.hovered ? ColorConst.hoverColor : ColorConst.secondaryColor
                                radius: 10
                            }
                            contentItem: Text {
                                text: "Load"
                                color: ColorConst.primaryColor
                                font.bold: true
                                anchors.centerIn: parent
                                font.pointSize: FormatConst.smallFontSize
                            }
                            padding: FormatConst.defaultPadding
                            FolderDialog {
                                id: loadReconstructionDialog
                                property string chosenDir: ""
                                onAccepted: {
                                    chosenDir = loadReconstructionDialog.selectedFolder
                                    backend.upload_reconstruction(chosenDir)
                                    settingsStatus.data = true
                                }
                            }
                            onClicked: {
                                loadReconstructionDialog.open()
                            }
                        }
                         Button {
                            id: clearReconstructionButton
                            font.pointSize: FormatConst.defaultFontSize
                            font.bold: true
                            background: Rectangle {
                                color: clearReconstructionButton.hovered ? ColorConst.hoverColor : ColorConst.secondaryColor
                                radius: 10
                            }
                            contentItem: Text {
                                text: "Clear"
                                color: ColorConst.primaryColor
                                font.bold: true
                                anchors.centerIn: parent
                                font.pointSize: FormatConst.smallFontSize
                            }
                            padding: FormatConst.defaultPadding
                             onClicked: {
                                backend.clear_reconstruction()

                             }
                        }

                       /* RoundButton_ {
                            id: clearReconstructionButton
                            icon.source: "../icons/clear.png"
                            icon.width: 35
                            icon.height: 35
                            icon.color: clearReconstructionButton.hovered ? ColorConst.hoverColor : ColorConst.secondaryColor
                            Layout.alignment: Qt.AlignCenter
                        }*/
                    }
                }

                /*delegate: Item {
                    width: parent.width
                    height: 50
                
                    RowLayout {
                        anchors.fill: parent
                        spacing: 10

                        Label {
                            text: modelData.label
                            Layout.alignment: Qt.AlignLeft
                            width: 100
                        }

                        TextField {
                            id: textField
                            text: modelData.input
                            Layout.fillWidth: true
                        }
                    }
                }*/
            }

            RowLayout {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                Layout.margins: FormatConst.defaultMargin

                Button {
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        applyChanges();
                        settingsStatus.data = true
                    }
                    background: Rectangle {
                        color: ColorConst.secondaryColor
                        radius: 10
                    }
                    contentItem: Text {
                        text: "Apply"
                        color: ColorConst.primaryColor
                        font.bold: true
                        anchors.centerIn: parent
                        font.pointSize: FormatConst.smallFontSize
                    }
                    padding: FormatConst.defaultPadding
                }

                Button {
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        settingsStatus.data = true
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
    SuccessWindow {
        id: successWindow
        visible: false
    }
}