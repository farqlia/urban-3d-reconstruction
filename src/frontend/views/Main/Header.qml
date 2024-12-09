import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Dialogs

import Constants
import Components

Rectangle {
    id: header
    color: ColorConst.primaryColor

    RowLayout {
        anchors.fill: parent
        anchors.margins: FormatConst.defaultMargin
        spacing: FormatConst.defaultSpacing

        LayoutItemProxy {
            target: buttonFiles
            width: FormatConst.headerButtonSize
            height: FormatConst.headerButtonSize
        }

        LayoutItemProxy {
            target: optionBuildMode
            width: 200
            height: 40
        }

        LayoutItemProxy {
            target: buttonRun
            width: FormatConst.headerButtonSize
            height: FormatConst.headerButtonSize
        }
        LayoutItemProxy {
            target: buttonSave
            width: FormatConst.headerButtonSize
            height: FormatConst.headerButtonSize
        }
        Spacer_{}

        LayoutItemProxy {
            target: titleCard
            width: FormatConst.headerTitleCardWidth
            height: FormatConst.headerTitleCardHeight
            anchors.horizontalCenter: parent.horizontalCenter
        }

        LayoutItemProxy {
            target: buttonParams
            width: FormatConst.headerButtonSize
            height: FormatConst.headerButtonSize
        }

        LayoutItemProxy {
            target: buttonSettings
            width: FormatConst.headerButtonSize
            height: FormatConst.headerButtonSize
        }
    }

    RoundButton_ {
        id: buttonFiles
        icon.source: "../icons/folder.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        icon.color: buttonFiles.hovered? ColorConst.hoverColor : ColorConst.secondaryColor

        onClicked: {
            selectedTab.data = 0
        }
    }
    RoundButton_ {
        id: buttonParams
        icon.source: "../icons/equalizer.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        icon.color: buttonParams.hovered? ColorConst.hoverColor : ColorConst.secondaryColor
        onClicked: {
            selectedTab.data = 1
        }
    }
    RoundComboBox_ {
        id: optionBuildMode
        model: [LangConst.comboBoxPointCloud, LangConst.comboBoxSplats, LangConst.comboBoxCategorization]
    }
    RoundButton_ {
        id: buttonRun
        icon.source: "../icons/play.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        icon.color: buttonRun.hovered? ColorConst.hoverColor : ColorConst.secondaryColor

        onClicked: {
            switch (optionBuildMode.currentText) {
                case LangConst.comboBoxPointCloud:
                    buildRunCloud.func()
                    break;
                case LangConst.comboBoxSplats:
                    buildRunSplats.func()
                    break;
                case LangConst.comboBoxCategorization:
                    buildRunCategorization.func()
                    break;
            }
        }
    }
    RoundButton_ {
        id: buttonSave
        icon.source: "../icons/save.webp"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        icon.color: buttonSave.hovered? ColorConst.hoverColor : ColorConst.secondaryColor

        FolderDialog {
            id: saveFileDialog
            property string destinationPath: ""
            onAccepted: {
                destinationPath = saveFileDialog.selectedFolder
                switch (optionBuildMode.currentText) {
                    case LangConst.comboBoxPointCloud:
                        backend.save_cloud(destinationPath)
                        break;
                    case LangConst.comboBoxSplats:
                        backend.save_gaussian_model(destinationPath)
                        break;
                    case LangConst.comboBoxCategorization:
                        backend.save_segmented_model(destinationPath)
                        break;
                }
            }
        }

        onClicked: {
            saveFileDialog.open();
        }
    }
    TitleCard_ {
        id: titleCard
        text: "Urb3D"
        imageSource: "../icons/logo.png"
    }
    RoundButton_ {
        id: buttonSettings
        icon.source: "../icons/cog.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        icon.color: buttonSettings.hovered? ColorConst.hoverColor : ColorConst.secondaryColor

        onClicked: {
            isSettingsOpen.data = true
        }
    }
}