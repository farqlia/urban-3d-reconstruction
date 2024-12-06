import QtQuick
import QtCore
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

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
            
            

        }
    }
}