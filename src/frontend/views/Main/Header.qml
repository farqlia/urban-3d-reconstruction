import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

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
            target: buttonParams
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
        Spacer_{}

        LayoutItemProxy {
            target: titleCard
            width: FormatConst.headerTitleCardWidth
            height: FormatConst.headerTitleCardHeight
            anchors.horizontalCenter: parent.horizontalCenter
        }


        LayoutItemProxy {
            target: buttonSettings
            width: FormatConst.headerButtonSize
            height: FormatConst.headerButtonSize
        }

        LayoutItemProxy {
            target: buttonInfo
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
            isFileListOpen.data = !isFileListOpen.data
        }
    }
    RoundButton_ {
        id: buttonParams
        icon.source: "../icons/equalizer.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        icon.color: buttonParams.hovered? ColorConst.hoverColor : ColorConst.secondaryColor
        onClicked: {
            isParametersOpen.data = true
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
            isBuildOpen.data = true;
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
    RoundButton_ {
        id: buttonInfo
        icon.source: "../icons/info.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        icon.color: buttonInfo.hovered? ColorConst.hoverColor : ColorConst.secondaryColor
    }
}