import sys
import os
from PySide6.QtQml import QQmlEngine
from PySide6.QtCore import QObject, QUrl, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication, QLabel, QHBoxLayout, QStackedLayout
from PySide6.QtQuickWidgets import QQuickWidget
from models.basic_model import BasicModelStr, BasicModelList, BasicModelInt
from pyntcloud import PyntCloud

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rendering.render_point_cloud import PointCloudGLWidget, prepare_point_cloud

class MainWindow(QMainWindow):
    def __init__(self, backend, engine_manager, opengl_widget):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Urb3D - Urban 3D reconstruction and segmentation")
        self.setGeometry(100, 100, 1600, 900)
        self.setFixedSize(1600, 900)

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        
        central_widget.setStyleSheet(
            "background-color: #282C34"
        )

        header = engine_manager.load_component("src/frontend/views/Main/Header.qml")
        left_pane = engine_manager.load_component("src/frontend/views/Main/BodyLeftPane.qml")
        right_pane = engine_manager.load_component("src/frontend/views/Main/BodyRightPane.qml")
        footer = engine_manager.load_component("src/frontend/views/Main/Footer.qml")

        # header_scope = header.rootObject()
        # left_pane_scope = left_pane.rootObject()
        # right_pane_scope = right_pane.rootObject()
        # footer_scope = footer.rootObject()

        # backend.add_scope(header_scope)
        # backend.add_scope(left_pane_scope)
        # backend.add_scope(right_pane_scope)
        # backend.add_scope(footer_scope)

        header.setMaximumHeight(100)
        footer.setMaximumHeight(20)

        body = self.setup_body(left_pane, right_pane, opengl_widget)

        body.setMaximumHeight(700)

        central_layout.addWidget(header)
        central_layout.addWidget(body)
        central_layout.addWidget(footer)

        self.setCentralWidget(central_widget)
    
    def setup_body(self, left_pane, right_pane, opengl_widget):
        body_container = QWidget()
        body_layout = QHBoxLayout(body_container)

        left_pane_container = QWidget()
        left_pane_layout = QVBoxLayout(left_pane_container)

        right_pane_container = QWidget()
        right_pane_layout = QStackedLayout(right_pane_container)
        right_pane_layout.setStackingMode(QStackedLayout.StackAll)

        left_pane_layout.addWidget(left_pane)
        right_pane_layout.addWidget(opengl_widget)
        # right_pane_layout.addWidget(right_pane)

        # right_pane_layout.setAlignment(opengl_widget, Qt.AlignCenter) # XDDDDDDDDDDDDDDDDDDDDD

        left_pane_container.setMaximumWidth(300)
        right_pane_container.setMaximumWidth(1200)

        body_layout.addWidget(left_pane_container)
        body_layout.addWidget(right_pane_container)

        return body_container
    
class EngineManager(QObject):
    def __init__(self, backend):
        super().__init__()

        self.engine = QQmlEngine()
        self.engine.rootContext().setContextProperty("fileList", backend.file_list)
        self.engine.rootContext().setContextProperty("directoryPath", backend.directory_path)
        self.engine.addImportPath("src/frontend/views")
        # engine.loadFromModule("Main", "MainWindow")
    
    def load_component(self, qml_file):
        widget = QQuickWidget(self.engine, None)
        widget.setSource(QUrl.fromLocalFile(qml_file))
        widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        return widget


class Backend:
    def __init__(self):
        self._directory_path = BasicModelStr()
        self._file_list = BasicModelList()
        self._selected_tab = 
    
    @property
    def directory_path(self):
        return self._directory_path

    @property
    def file_list(self):
        return self._file_list

    def add_scope(self, scope):
        scopes.append(scope)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    backend = Backend()
    engine_manager = EngineManager(backend)

    # point_cloud_file = "../data/c7_sparse.ply"
    # point_cloud = PyntCloud.from_file(point_cloud_file)
    # prepare_point_cloud(point_cloud)

    # opengl_widget = PointCloudGLWidget(point_cloud.points)
    opengl_widget = QLabel("XD")
    opengl_widget.setFixedSize(50,50)

    window = MainWindow(backend, engine_manager, opengl_widget)
    window.show()

    sys.exit(app.exec())
