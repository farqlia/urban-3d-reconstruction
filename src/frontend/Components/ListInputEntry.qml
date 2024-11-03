import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import Constants

Item {
    id: listInputEntry
    width: parent.width
    height: 50

    property string labelText: ""
    property string inputText: textField.text

    onLabelTextChanged: {
        label.text = labelText
    }

    Border {
        width: parent.width
        height: parent.height

        RowLayout {
            anchors.fill: parent
            anchors.margins: FormatConst.smallMargin

            Label {
                id: label
                text: labelText
                Layout.preferredWidth: 100
                color: ColorConst.secondaryColor
                font.pointSize: FormatConst.smallFontSize
                font.bold: true
                Layout.alignment: Qt.AlignLeft
            }

            Spacer {}

            TextField {
                id: textField
                Layout.preferredWidth: 75
                color: ColorConst.primaryColor
                placeholderText: "..."
                placeholderTextColor: ColorConst.primaryColor
                horizontalAlignment: Text.AlignHCenter
                background: Rectangle {
                    color: ColorConst.secondaryColor
                    radius: FormatConst.defaultRadius
                }
            }
        }
    }
}