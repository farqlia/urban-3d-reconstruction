import sys
import os
from PySide6.QtQml import QQmlEngine
from PySide6.QtCore import QObject, QUrl, Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication, QLabel, QHBoxLayout, QStackedLayout, QFileDialog
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface

if __name__ == '__main__':
    app = QApplication(sys.argv)
    backend = Backend()
    engine_manager = EngineManager(backend)

    QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)

    point_cloud_file = "data/360_v2/room/sparse/sparse.ply"
    point_cloud = PyntCloud.from_file(point_cloud_file)
    prepare_point_cloud(point_cloud)

    opengl_widget = PointCloudGLWidget(point_cloud.points)
    # opengl_widget = QLabel("XD")
    # opengl_widget.setFixedSize(50,50)

    window = MainWindow(backend, engine_manager, opengl_widget)
    window.show()

    sys.exit(app.exec())
