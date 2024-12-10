
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Components
import Constants

Rectangle {
    id: parametersWindow
    color: ColorConst.primaryColor

    width: FormatConst.popupSmallWidth
    height: 450

    function getCopyVars() {
        var tempVars = [];
        for (var i = 0; i < settingsVars.data.length; i++) {
            tempVars.push(settingsVars.data[i]);
        }
        return tempVars;
    }

    function applyChanges() {
        var tempVars = [];
        tempVars.push(strategyInput.currentText);
        tempVars.push(stepsInput.text);
        tempVars.push(capInput.text);
        tempVars.push(refineInput.text);
        tempVars.push(shInput.currentText);
        parametersVars.data = tempVars;
    }

    Border_ {
        width: parent.width
        height: parent.height

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: FormatConst.defaultMargin

            RoundButton_ {
                icon.source: "../icons/equalizer.png"
                Layout.alignment: Qt.AlignHCenter
                icon.color: ColorConst.secondaryColor
                icon.width: RoundButtonConst.headerImageRadius
                icon.height: RoundButtonConst.headerImageRadius
            }

            GridLayout {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                Layout.margins: FormatConst.defaultMargin
                columns: 2
                rowSpacing: 20
                columnSpacing: 10

                Label {
                    text: "Strategy"
                    color: ColorConst.secondaryColor
                    font.pointSize: FormatConst.smallFontSize
                    font.bold: true
                }

                RoundComboBox_ {
                    id: strategyInput
                    model: ["default", "mcmc"]
                    additionalPadding: 10
                    implicitWidth: 100
                    implicitHeight: 30
                }

                Label {
                    text: "Max steps"
                    color: ColorConst.secondaryColor
                    font.pointSize: FormatConst.smallFontSize
                    font.bold: true
                }

                TextField {
                    id: stepsInput
                    text: parametersVars.data[1]
                    Layout.preferredWidth: 100
                    color: ColorConst.primaryColor
                    background: Rectangle {
                        color: ColorConst.secondaryColor
                        radius: FormatConst.defaultRadius
                    }
                }

                Label {
                    text: "Cap max"
                    color: ColorConst.secondaryColor
                    font.pointSize: FormatConst.smallFontSize
                    font.bold: true
                }

                TextField {
                    id: capInput
                    text: parametersVars.data[2]
                    Layout.preferredWidth: 100
                    color: ColorConst.primaryColor
                    background: Rectangle {
                        color: ColorConst.secondaryColor
                        radius: FormatConst.defaultRadius
                    }
                }

                Label {
                    text: "Refine every (iterations)"
                    color: ColorConst.secondaryColor
                    font.pointSize: FormatConst.smallFontSize
                    font.bold: true
                }

                TextField {
                    id: refineInput
                    text: parametersVars.data[3]
                    Layout.preferredWidth: 100
                    color: ColorConst.primaryColor
                    background: Rectangle {
                        color: ColorConst.secondaryColor
                        radius: FormatConst.defaultRadius
                    }
                }

                Label {
                    text: "Spherical harmonics degrees"
                    color: ColorConst.secondaryColor
                    font.pointSize: FormatConst.smallFontSize
                    font.bold: true
                }

                RoundComboBox_ {
                    id: shInput
                    model: ["1", "2", "3"]
                    additionalPadding: 10
                    implicitWidth: 100
                    implicitHeight: 30
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
                        parametersStatus.data = true
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
                        parametersStatus.data = true
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