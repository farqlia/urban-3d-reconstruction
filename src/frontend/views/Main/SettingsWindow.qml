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
    height: 500

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
            spacing: FormatConst.defaultPadding
            anchors.topMargin: FormatConst.defaultMargin

            RoundButton_ {
                icon.source: "../icons/cog.png"
                Layout.alignment: Qt.AlignHCenter
                icon.color: ColorConst.secondaryColor
                icon.width: RoundButtonConst.headerImageRadius
                icon.height: RoundButtonConst.headerImageRadius
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignHCenter
                spacing: FormatConst.defaultMargin

                CheckBox {
                    id: awayRendering
                    text: "3rd party rendering"
                    checked: !renderingType.data
                    onCheckedChanged: {
                        homeRendering.checked = !checked
                    }
                }

                CheckBox {
                    id: homeRendering
                    text: "Own rendering"
                    checked: renderingType.data
                    onCheckedChanged: {
                        awayRendering.checked = !checked
                    }
                }
            }

            ColumnLayout {
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: FormatConst.defaultMargin
                spacing: FormatConst.defaultPadding
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
                                try {
                                    chosenDir = loadReconstructionDialog.selectedFolder;
                                    backend.upload_reconstruction(chosenDir);
                                    messageDialog.title = "Success"
                                    messageDialog.text = "Reconstruction uploaded successfully!";
                                    messageDialog.open();
                                } catch (error) {
                                    messageDialog.title = "Error"
                                    messageDialog.text = "Couldn't upload reconstruction";
                                    messageDialog.open();
                                }
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
                            messageDialog.title = "Success"
                            messageDialog.text = "Reconstruction cleared successfully!"
                            messageDialog.open()
                        }
                    }
                }
                RowLayout {
                    id: contentModel
                    // anchors.fill: parent
                    spacing: FormatConst.smallPadding
                    anchors.horizontalCenter: parent.horizontalCenter

                    Text {
                        text: "Gaussian model ckpts  "
                        Layout.alignment: Qt.AlignCenter
                        color: ColorConst.secondaryColor
                        font.pointSize: FormatConst.smallFontSize
                        font.bold: true
                    }

                    Button {
                        id: loadGModelButton
                        font.pointSize: FormatConst.defaultFontSize
                        font.bold: true
                        background: Rectangle {
                            color: loadGModelButton.hovered ? ColorConst.hoverColor : ColorConst.secondaryColor
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
                            id: loadGModelDialog

                            property string chosenDir: ""
                            onAccepted: {
                                try {
                                    chosenDir = loadGModelDialog.selectedFolder;
                                    backend.upload_gaussian_ckpts(chosenDir);
                                    messageDialog.title = "Success"
                                    messageDialog.text = "Model uploaded successfully!";
                                    messageDialog.open();
                                } catch (error) {
                                    messageDialog.title = "Error"
                                    messageDialog.text = "Couldn't upload model";
                                    messageDialog.open();
                                }
                            }
                        }
                        onClicked: {
                            loadGModelDialog.open()
                        }
                    }
                    Button {
                        id: clearModelButton
                        font.pointSize: FormatConst.defaultFontSize
                        font.bold: true
                        background: Rectangle {
                            color: clearModelButton.hovered ? ColorConst.hoverColor : ColorConst.secondaryColor
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
                            backend.clear_gaussian_model()
                            messageDialog.title = "Success"
                            messageDialog.text = "Gaussian model cleared successfully!"
                            messageDialog.open()
                        }
                    }
                }
            }

            ListView {
                id: listView
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignHCenter
                Layout.margins: FormatConst.defaultMargin
                //spacing: FormatConst.smallPadding
                //model: [1]
                model: settingsVars ? getCopyVars() : []

                delegate: Item {
                    width: parent.width
                    height: 50

                    RowLayout {
                        anchors.fill: parent
                        spacing: 10

                        Label {
                            text: modelData.label
                            Layout.alignment: Qt.AlignLeft
                            width: 100
                            color: ColorConst.secondaryColor
                        }

                        TextField {
                            id: textField
                            text: modelData.input
                            Layout.fillWidth: true
                            color: ColorConst.primaryColor
                            background: Rectangle {
                                color: ColorConst.secondaryColor
                                radius: FormatConst.defaultRadius
                            }
                        }
                    }
                }
            }

            RowLayout {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                Layout.margins: FormatConst.defaultMargin

                Button {
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        applyChanges();
                        if (awayRendering.checked)
                            renderingType.data = 0;
                        else if (homeRendering.checked)
                            renderingType.data = 1;
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
    SuccessWindow {
        id: successWindow
        visible: false
    }

    MessageDialog {
        id: messageDialog
    }
}