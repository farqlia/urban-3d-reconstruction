import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Constants

Rectangle {
    color: "transparent"

    RowLayout {
        anchors.fill: parent

        Image {
            id: imageTitleCard
            Layout.preferredWidth: FormatConst.headerTitleCardHeight
            Layout.preferredHeight: FormatConst.headerTitleCardHeight
            fillMode: Image.PreserveAspectFit
            Layout.alignment: Qt.AlignLeft
        }

        Spacer {}

        Text {
            id: textTitleCard
            color: "white"
            font.pointSize: TitleCardConst.fontSize
            font.bold: true
            Layout.alignment: Qt.AlignRight
        }
    }

    property alias imageSource: imageTitleCard.source
    property alias text: textTitleCard.text
}