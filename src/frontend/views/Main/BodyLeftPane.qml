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
            currentIndex: selectedTab ? selectedTab.data : 0

            LayoutItemProxy {
                target: loadedImagesTab
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
                Layout.alignment: Qt.AlignHCenter

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

    RoundButton_ {
        id: buttonOpenDialogWindow
        icon.source: "../icons/folder-click.png"
        icon.width: 35
        icon.height: 35
        icon.color: buttonOpenDialogWindow.hovered? ColorConst.hoverColor : ColorConst.secondaryColor
        onClicked: {
            isDialogOpen.data = true
        }
    }
}