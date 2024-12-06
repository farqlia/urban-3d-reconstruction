
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Components
import Constants

Rectangle {
    id: loadingWindow
    color: ColorConst.primaryColor

    width: FormatConst.popupWidth
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
                spacing: FormatConst.smallPadding
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
                        }

                        TextField {
                            id: textField
                            text: modelData.input
                            Layout.fillWidth: true
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
}