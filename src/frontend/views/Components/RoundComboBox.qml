import QtQuick
import QtQuick.Controls

import Constants

ComboBox {
    id: comboBox
    property int additionalPadding: 0

    contentItem: Text {
        leftPadding: 10
        rightPadding: comboBox.indicator.width + comboBox.spacing + additionalPadding

        text: comboBox.displayText
        font.bold: true
        color: ColorConst.primaryColor
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    indicator: Item {
        x: comboBox.width - width - comboBox.rightPadding - 5
        y: comboBox.topPadding + (comboBox.availableHeight - height) / 2
        width: 15
        height: 15
        Image {
            width: parent.width
            height: parent.height
            source: "../icons/down.png"
            fillMode: Image.PreserveAspectFit
        }
    }

    background: Rectangle {
        implicitHeight: parent.height
        implicitWidth: parent.width
        color: ColorConst.secondaryColor
        radius: 10
    }

    delegate: ItemDelegate {
        id: delegate

        required property var model
        required property int index

        width: comboBox.width
        contentItem: Text {
            text: delegate.model[comboBox.textRole]
            color: highlighted ? ColorConst.primaryColor : ColorConst.secondaryColor
            font.bold: true
            verticalAlignment: Text.AlignVCenter
        }
        highlighted: comboBox.highlightedIndex == index

        background: Rectangle {
            color: highlighted ? ColorConst.hoverColor : "transparent"
            radius: 10
        }
    }

    popup: Popup {
        width: comboBox.width
        implicitHeight: contentItem.implicitHeight
        padding: 1

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: comboBox.popup.visible ? comboBox.delegateModel : null
            currentIndex: comboBox.highlightedIndex

            ScrollIndicator.vertical: ScrollIndicator {}
        }

        background: Rectangle {
            color: ColorConst.primaryColor
            border.color: ColorConst.secondaryColor
            border.width: 2
            radius: 10
        }
    }
}