import sys
import os
import asyncio
import subprocess
from PySide6.QtQml import QQmlEngine
from PySide6.QtCore import QObject, QUrl, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QApplication, QLabel, QHBoxLayout, QStackedLayout, QFileDialog
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from models.basic_model import BasicModelStr, BasicModelList, BasicModelInt, BasicModelBool, BasicModelFunc
from pyntcloud import PyntCloud

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rendering.render_point_cloud import PointCloudGLWidget, prepare_point_cloud

class MainWindow(QMainWindow):
    def __init__(self, backend, engine_manager, opengl_widget):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Urb3D - Urban 3D reconstruction and segmentation")
        self.setGeometry(100, 100, 1600, 900)
        self.setFixedSize(1600, 900)

        self.backend = backend
        self.engine_manager = engine_manager

        self.connect_backend()

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        
        central_widget.setStyleSheet(
            "background-color: #282C34"
        )

        header = self.engine_manager.load_component("src/frontend/views/Main/Header.qml")
        left_pane = self.engine_manager.load_component("src/frontend/views/Main/BodyLeftPane.qml")
        right_pane = self.engine_manager.load_component("src/frontend/views/Main/BodyRightPane.qml")
        footer = self.engine_manager.load_component("src/frontend/views/Main/Footer.qml")

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
        body_container.setWindowModality(Qt.WindowModality.ApplicationModal)

        left_pane_container = QWidget()
        left_pane_layout = QVBoxLayout(left_pane_container)

        right_pane_container = QWidget()
        right_pane_layout = QStackedLayout(right_pane_container)
        right_pane_layout.setStackingMode(QStackedLayout.StackAll)

        left_pane_layout.addWidget(left_pane)
        # right_pane_layout.addWidget(opengl_widget)
        # right_pane_layout.addWidget(right_pane)

        # right_pane_layout.setAlignment(opengl_widget, Qt.AlignCenter) # XDDDDDDDDDDDDDDDDDDDDD

        left_pane_container.setMaximumWidth(300)
        right_pane_container.setMaximumWidth(1200)

        body_layout.addWidget(left_pane_container)
        body_layout.addWidget(right_pane_container)

        return body_container

    def connect_backend(self):
        self.backend.setup_open_dialog_handler(self.open_dialog)
        self.backend.setup_build_run_handler(self.open_progress_bar)

    def open_dialog(self):
        dialog = QFileDialog.getExistingDirectoryUrl(self, "Choose directory", "", QFileDialog.Option.ShowDirsOnly)
        dir_path = QUrl(dialog).toLocalFile()
        if dir_path:
            self.backend.file_list.data = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        else:
            self.backend.file_list.data = []
        
    def open_progress_bar(self):
        overlay = QWidget(self)
        overlay.setStyleSheet(
            "background: rgba(0,0,0,80)"
        )
        parent_rect = self.rect()
        overlay_width = parent_rect.width() // 4
        overlay_height = parent_rect.height() // 4
        overlay.setGeometry(
            (parent_rect.width() - overlay_width) // 2,
            (parent_rect.height() - overlay_height) // 2,
            overlay_width,
            overlay_height
        )
        label = QLabel("LOADING")
        layout = QVBoxLayout(overlay)
        layout.addWidget(label)
        overlay.setLayout(layout)
        overlay.show()
    
class EngineManager(QObject):
    def __init__(self, backend):
        super().__init__()

        self.engine = QQmlEngine()
        self.engine.rootContext().setContextProperty("fileList", backend.file_list)
        self.engine.rootContext().setContextProperty("selectedTab", backend.selected_tab)
        self.engine.rootContext().setContextProperty("openDialog", backend.open_dialog)
        self.engine.rootContext().setContextProperty("buildRunReconstruction", backend.reconstruction)
        self.engine.addImportPath("src/frontend/views")
        # engine.loadFromModule("Main", "MainWindow")
    
    def load_component(self, qml_file):
        widget = QQuickWidget(self.engine, None)
        widget.setSource(QUrl.fromLocalFile(qml_file))
        widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        return widget


class Backend:
    def __init__(self):
        self._file_list = BasicModelList()
        self._selected_tab = BasicModelInt()
        self._open_dialog = BasicModelBool()
        self._build_script = BasicModelBool()
        self._reconstruction = BasicModelFunc(self.reconstruction_func)
    
    @property
    def file_list(self):
        return self._file_list

    @property
    def selected_tab(self):
        return self._selected_tab

    @property
    def open_dialog(self):
        return self._open_dialog

    @property
    def reconstruction(self):
        return self._reconstruction

    def reconstruction_func(self):
        # ADD REQUIRED ARGS like this -> (--input,INPUT,--output,OUTPUT) etc
        self.run_script("scripts/colmap_reconstruction.py")
    
    def run_script(self, script_path, *args):
        self._build_script.data = True # we trigger progress bar, should be numeric value for progress or something
        self.handle_exec_script(script_path, *args)
    
    async def async_execute_script(self, script_path, *args):
        try:
            _args = ' '.join(map(str, args))
            # HERE CHANGE TO SOME COMMON SOURCE
            command = ["bash", "-c", f"source venv-frontend/bin/activate && python {script_path} {_args}"]
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            return result.stdout, result.stderr, result.returncode
        
        except subprocess.CalledProcessError as e:
            return e.stdout, e.stderr, e.returncode
    
    def setup_open_dialog_handler(self, func):
        self._open_dialog.dataChanged.connect(lambda: self.handle_open_dialog(func))

    def handle_open_dialog(self, func):
        if self._open_dialog.data:
            self._open_dialog.data = False
            func()

    def setup_build_run_handler(self, func):
        self._build_script.dataChanged.connect(lambda: self.handle_build_run(func))
    
    def handle_build_run(self, func):
        if self._build_script:
            self._build_script.data = False
            func()

    def handle_exec_script(self, script_path, *args):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        task = event_loop.create_task(self.async_execute_script(script_path, *args))
        task.add_done_callback(lambda callback: self.process_script_result(callback.result(), event_loop))
        event_loop.run_forever()

    def process_script_result(self, result, event_loop):
        # do sth, this for now
        stdout, stderr, returncode = result
        if (returncode == 0):
            print(f"Success: {stdout}")
        else:
            print(f"Error: {stderr}")
        event_loop.stop()

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
