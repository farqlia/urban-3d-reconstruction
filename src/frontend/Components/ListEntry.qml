import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants

Item {
    id: listEntry
    width: parent.width
    height: 50

    property string text: ""

    Border {
        color: ColorConst.secondaryColor
        width: parent.width
        height: parent.height
        border.color: "transparent"

        RowLayout {
            anchors.fill: parent
            anchors.margins: FormatConst.smallMargin

            Image {
                source: "../icons/image.png"
                Layout.preferredWidth: FormatConst.listEntryImageSize
                Layout.preferredHeight: FormatConst.listEntryImageSize
                fillMode: Image.PreserveAspectFit
                Layout.alignment: Qt.AlignLeft
            }
            
            Spacer {}

            Text {
                text: listEntry.text
                Layout.preferredWidth: 150
                color: ColorConst.primaryColor
                font.pointSize: FormatConst.smallFontSize
                font.bold: true
                Layout.alignment: Qt.AlignRight
                elide: Text.ElideRight
            }
        }
    }
}