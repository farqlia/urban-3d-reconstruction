import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants
import Components

Rectangle {
    id: bodyRightPaneLT
    color: ColorConst.primaryColor

    Border_ {
        anchors.fill: parent
    
        GridLayout {
            rows: 2
            columns: 3
            anchors.fill: parent
            anchors.margins: FormatConst.smallMargin

            LayoutItemProxy {
                target: coordsX
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }
            LayoutItemProxy {
                target: coordsY
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }
            LayoutItemProxy {
                target: coordsZ
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }
            LayoutItemProxy {
                target: coordsXValue
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }
            LayoutItemProxy {
                target: coordsYValue
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }
            LayoutItemProxy {
                target: coordsZValue
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }
        }
    }
    Text {
        id: coordsX
        text: "X:"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
        font.bold: true
    }
    Text {
        id: coordsY
        text: "Y:"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
        font.bold: true
    }
    Text {
        id: coordsZ
        text: "Z:"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.defaultFontSize
        font.bold: true
    }
    Text {
        id: coordsXValue
        text: "10"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.smallFontSize
    }
    Text {
        id: coordsYValue
        text: "10"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.smallFontSize
    }
    Text {
        id: coordsZValue
        text: "10"
        color: ColorConst.informativeColor
        font.pointSize: FormatConst.smallFontSize
    }
}