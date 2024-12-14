import sys
import os
from PySide6.QtQml import QQmlEngine
from PySide6.QtCore import QObject, QUrl, Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication, QLabel, QHBoxLayout, QStackedLayout, QFileDialog
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface

from src.backend.controller import Controller
from src.frontend.view import View
from src.urb3d.pipeline.backend import Backend

if __name__ == '__main__':
    app = QApplication(sys.argv)
    backend = Backend()
    controller = Controller(backend)
    view = View(controller)

    view.run()
    sys.exit(app.exec())

    '''
    QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)

    point_cloud_file = "data/360_v2/room/sparse/sparse.ply"
    point_cloud = PyntCloud.from_file(point_cloud_file)
    prepare_point_cloud(point_cloud)

    opengl_widget = PointCloudGLWidget(point_cloud.points)
    # opengl_widget = QLabel("XD")
    # opengl_widget.setFixedSize(50,50)

    window = MainWindow(backend, engine_manager, opengl_widget)
    window.show()

    sys.exit(app.exec())'''
