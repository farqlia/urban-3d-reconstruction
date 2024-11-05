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

    property int currentTabIndex: 0
    property string currentBuildMode: LangConst.comboBoxPointCloud

    onCurrentTabIndexChanged: {
        stackLayout.currentIndex = currentTabIndex
    }

    onCurrentBuildModeChanged: {

    }

    Border_{
        anchors.fill: parent
        width: 260

        StackLayout {
            id: stackLayout
            anchors.fill: parent
            currentIndex: currentTabIndex

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

    Tab_ {
        id: loadedImagesTab

        model: fileList ? fileList.data : []
        placeholder: Item {
            anchors.fill: parent

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
        }
    }
    Tab_ {
        id: settingParametersTab
        model: bodyLeftPane.currentBuildMode === LangConst.comboBoxSplats ? [LangConst.paramSplatCount] : []
        placeholder: Item {
            anchors.fill: parent

            Text {
                // TODO: Repair text formatting xdd
                text: "           Setting\nparameters images"
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                color: ColorConst.secondaryColor
                font.pointSize: FormatConst.defaultFontSize
                font.bold: true
            }
        }
    }
    RoundButton_ {
        id: buttonOpenDialogWindow
        icon.source: "../icons/folder-click.png"
        icon.width: 40
        icon.height: 40
        onClicked: {
            fileDialog.open()
        }
    }
    FolderDialog {
        id: fileDialog
        currentFolder: "/home/frafau/Pictures"
        onAccepted: directoryPath.data = selectedFolder
    }
}