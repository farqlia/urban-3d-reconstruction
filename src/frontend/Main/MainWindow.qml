import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Components
import Constants

ApplicationWindow {
    width: 1600
    height: 900
    maximumWidth: 1920
    maximumHeight: 1080
    minimumWidth: 1280
    minimumHeight: 720
    visible: true
    title: "Urb3D - Urban 3D reconstruction and segmentation"

    Rectangle {
        anchors.fill: parent
        color: ColorConst.primaryColor

        ColumnLayout {
            id: appWindowLayout
            anchors.fill: parent
            anchors.margins: FormatConst.defaultMargin
            
            RowLayout {
                id: header
                Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
                Layout.fillWidth: true
                height: FormatConst.headerHeight
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

                Spacer_ {}

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
                    target: titleCard
                    width: FormatConst.headerTitleCardWidth
                    height: FormatConst.headerTitleCardHeight
                }

                Spacer_ {}
                Spacer_ {}
                Spacer_ {}

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

            RowLayout {
                id: mainLayout
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: FormatConst.defaultMargin
                Layout.bottomMargin: FormatConst.defaultMargin
                // height: 900

                Border_{
                    Layout.fillHeight: true
                    Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                    Layout.rightMargin: FormatConst.defaultMargin
                    width: 260

                    ColumnLayout {
                        id: leftMainLayout
                        anchors.fill: parent

                        LayoutItemProxy {
                            id: leftMainView
                            target: loadingImagesView
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                        }
                    }
                }

                Border_{
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter

                    // Image {
                    //     anchors.fill: parent
                    //     // Ay, you caught me hehexd
                    //     source: "../icons/caught.png"
                    // }

                    GridLayout {
                        id: rightMainLayout
                        anchors.fill: parent
                        columns: 2
                        rows: 2

                        Border_ {
                            width: 300
                            height: 80
                            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                            Layout.topMargin: FormatConst.defaultMargin
                            Layout.leftMargin: FormatConst.defaultMargin

                            GridLayout {
                                id: coordsLayout
                                rows: 2
                                columns: 3
                                anchors.fill: parent
                                anchors.margins: FormatConst.smallMargin

                                LayoutItemProxy {
                                    target: textCoordsX
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                LayoutItemProxy {
                                    target: textCoordsY
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                LayoutItemProxy {
                                    target: textCoordsZ
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                LayoutItemProxy {
                                    target: textCoordsXValue
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                LayoutItemProxy {
                                    target: textCoordsYValue
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }

                                LayoutItemProxy {
                                    target: textCoordsZValue
                                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                                }
                            }
                        }

                        Border_{
                            width: 70
                            height: 140
                            Layout.alignment: Qt.AlignRight | Qt.AlignTop
                            Layout.topMargin: FormatConst.defaultMargin
                            Layout.rightMargin: FormatConst.defaultMargin

                            ColumnLayout {
                                id: renderingModeLayout
                                anchors.fill: parent

                                LayoutItemProxy {
                                    target: buttonSplat3DMode
                                    width: RoundButtonConst.renderingModeRadius
                                    height: RoundButtonConst.renderingModeRadius
                                    Layout.alignment: Qt.AlignHCenter
                                    Layout.topMargin: FormatConst.smallMargin
                                }

                                Rectangle {
                                    width: parent.width
                                    height: FormatConst.defaultBorderWeight
                                    color: ColorConst.secondaryColor
                                }

                                LayoutItemProxy {
                                    target: buttonCategorization3DMode
                                    width: RoundButtonConst.renderingModeRadius
                                    height: RoundButtonConst.renderingModeRadius
                                    Layout.alignment: Qt.AlignHCenter
                                    Layout.bottomMargin: FormatConst.smallMargin
                                }
                            }
                        }

                        Border_ {
                            width: 200  
                            height: 170
                            Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                            Layout.bottomMargin: FormatConst.defaultMargin
                            Layout.leftMargin: FormatConst.defaultMargin
                            color: ColorConst.secondaryColor

                            ColumnLayout {

                            }
                        }
                        
                        Border_ {
                            width: 200
                            height: 100
                            Layout.alignment: Qt.AlignRight | Qt.AlignBottom
                            Layout.bottomMargin: FormatConst.defaultMargin
                            Layout.rightMargin: FormatConst.defaultMargin
                            border.color: "transparent"

                            RowLayout {
                                id: renderingActionLayout
                                anchors.fill: parent

                                LayoutItemProxy {
                                    target: buttonMoveAction
                                    width: RoundButtonConst.renderingModeRadius
                                    height: RoundButtonConst.renderingModeRadius
                                    Layout.alignment: Qt.AlignBottom
                                }

                                LayoutItemProxy {
                                    target: buttonRotateAction
                                    width: RoundButtonConst.renderingModeRadius
                                    height: RoundButtonConst.renderingModeRadius
                                    Layout.alignment: Qt.AlignBottom
                                }

                                LayoutItemProxy {
                                    target: buttonZoomAction
                                    width: RoundButtonConst.renderingModeRadius
                                    height: RoundButtonConst.renderingModeRadius
                                    Layout.alignment: Qt.AlignBottom
                                }
                            }
                        }
                    }
                }
            }

            RowLayout {
                id: footer
                Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
                Layout.fillWidth: true
                height: FormatConst.footerHeight

                LayoutItemProxy {
                    target: textLicense
                    Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                }

                Spacer_ {}

                LayoutItemProxy {
                    target: textBuildVersion
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                }
            }
        }
    }














    RoundButton_ {
        id: buttonFiles
        icon.source: "../icons/folder.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        onClicked: {
            settingParametersView.visible = false
            leftMainView.target = null
            loadingImagesView.visible = true
            leftMainView.target = loadingImagesView
        }
    }
    RoundButton_ {
        id: buttonParams
        icon.source: "../icons/equalizer.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        onClicked: {
            loadingImagesView.visible = false
            leftMainView.target = null
            settingParametersView.visible = true
            leftMainView.target = settingParametersView
        }
    }
    RoundComboBox_ {
        id: optionBuildMode
        model: ["Generate splats", "Generate categories"]
    }
    RoundButton_ {
        id: buttonRun
        icon.source: "../icons/run.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
        background: null
        onClicked: loadingWindow.open()
    }
    TitleCard_ {
        id: titleCard
        text: "Urb3D"
        imageSource: "../icons/logo.png"
    }
    // RoundButton_ {
    //     id: labelBuildStatus
    //     icon.source: "../icons/folder.png"
    //     icon.width: RoundButtonConst.headerImageRadius
    //     icon.height: RoundButtonConst.headerImageRadius
    // }
    RoundButton_ {
        id: buttonSettings
        icon.source: "../icons/cog.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
    }
    RoundButton_ {
        id: buttonInfo
        icon.source: "../icons/info.png"
        icon.width: RoundButtonConst.headerImageRadius
        icon.height: RoundButtonConst.headerImageRadius
    }
    RoundButton_ {
        id: buttonSplat3DMode
        icon.source: "../icons/3d-cube.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
    RoundButton_ {
        id: buttonCategorization3DMode
        icon.source: "../icons/categorization.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
    RoundButton_ {
        id: buttonMoveAction
        icon.source: "../icons/palm-of-hand.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
    RoundButton_ {
        id: buttonRotateAction
        icon.source: "../icons/360.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
    RoundButton_ {
        id: buttonZoomAction
        icon.source: "../icons/magnifier.png"
        icon.width: RoundButtonConst.renderingModeImageRadius
        icon.height: RoundButtonConst.renderingModeImageRadius
    }
    Text {
        id: textCoordsX
        text: "X:"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
        font.bold: true
    }
    Text {
        id: textCoordsY
        text: "Y:"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
        font.bold: true
    }
    Text {
        id: textCoordsZ
        text: "Z:"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
        font.bold: true
    }
    Text {
        id: textCoordsXValue
        text: "-100.00"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
    }
    Text {
        id: textCoordsYValue
        text: "100.00"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
    }
    Text {
        id: textCoordsZValue
        text: "100.00"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
    }
    Text {
        id: textLicense
        text: "TODO: CHOOSE LICENSE"
        color: ColorConst.secondaryColor
    }
    Text {
        id: textBuildVersion
        text: "version: 0.0.1-alpha-build"
        color: ColorConst.secondaryColor
        font.pointSize: 12
    }
    LoadingPopup_ {
        id: loadingWindow
        width: 500
        height: 200
    }
    Border_ {
        id: loadingImagesView
        color: "transparent"
        border.color: "transparent"
        visible: false

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: FormatConst.defaultMargin

            Text {
                text: "Uploaded images"
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                color: ColorConst.secondaryColor
                font.pointSize: FormatConst.defaultFontSize
                font.bold: true
            }
        }
    }
    Border_ {
        id: settingParametersView
        color: "transparent"
        border.color: "transparent"
        visible: false

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: FormatConst.defaultMargin

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
}
