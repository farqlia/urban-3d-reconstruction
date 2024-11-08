import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Dialogs
import QtQml

import Constants
import Components

Rectangle {
    id: bodyLeftPane
    color: ColorConst.primaryColor

    property string currentBuildMode: LangConst.comboBoxPointCloud

    Border_{
        anchors.fill: parent
        width: 260

        StackLayout {
            id: stackLayout
            anchors.fill: parent
            currentIndex: selectedTab.data

            LayoutItemProxy {
                target: loadedImagesTab
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            LayoutItemProxy {
                target: settingParametersTab
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }
    }

    Border_ {
        id: loadedImagesTab

        color: "transparent"
        border.color: "transparent"

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: FormatConst.defaultMargin

            RowLayout {
                Layout.fillWidth: true

                Text {
                    text: "Uploaded images"
                    Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                    color: ColorConst.secondaryColor
                    font.pointSize: FormatConst.defaultFontSize
                    font.bold: true
                }

                LayoutItemProxy {
                    target: buttonOpenDialogWindow
                    width: 50
                    height: 50
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }
            }

            ListView {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                Layout.fillHeight: true
                model: fileList ? fileList.data : []
                spacing: FormatConst.smallPadding

                delegate: ListEntry_ {
                    text: modelData
                }
            }
        }
    }


    Border_ {
        id: settingParametersTab

        color: "transparent"
        border.color: "transparent"

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: FormatConst.defaultMargin

            ColumnLayout {
                Layout.fillWidth: true

                Text {
                    text: "Setting"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    color: ColorConst.secondaryColor
                    font.pointSize: FormatConst.defaultFontSize
                    font.bold: true
                }

                Text {
                    text: "parameters"
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    color: ColorConst.secondaryColor
                    font.pointSize: FormatConst.defaultFontSize
                    font.bold: true
                }
            }

            ListView {
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                Layout.fillHeight: true
                model: []
                spacing: FormatConst.smallPadding

                delegate: ListEntry_ {
                    text: modelData
                }
            }
        }
    }
    RoundButton_ {
        id: buttonOpenDialogWindow
        icon.source: "../icons/folder-click.png"
        icon.width: 35
        icon.height: 35
        onClicked: {
            openDialog.data = true
        }
    }
}