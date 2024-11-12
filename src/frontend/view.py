from PySide6.QtCore import QObject, QUrl, Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtQuickWidgets import QQuickWidget

from .views.main_window import MainWindow
from .views.loading_window import LoadingWindow
from .view_engine_manager import EngineManager
from src.rendering.render_point_cloud import PointCloudGLWidget

class View:
    def __init__(self, controller):
        QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)
        self._controller = controller
        self._engine_manager = EngineManager()
        self._configure_engine_properties()
        self._configure_handlers()

        self._main_view = MainWindow(self._engine_manager)

    def run(self):
        self._create_renderer()
        self._main_view.show()

    def _configure_handlers(self):
        self._controller.configure_dialog_handler(self._open_dialog)
        self._controller.configure_build_run_handler(self._open_progress_bar)

    def _configure_engine_properties(self):
        self._engine_manager.set_qml_property("fileList", self._controller.get_file_list_qml())
        self._engine_manager.set_qml_property("selectedTab", self._controller.get_selected_tab_qml())
        self._engine_manager.set_qml_property("isOpenDialog", self._controller.get_is_dialog_open_qml())
        self._engine_manager.set_qml_property("buildRunCloud", self._controller.get_build_run_cloud_qml())
        self._engine_manager.set_qml_property("buildRunSplats", self._controller.get_build_run_splats_qml())
        self._engine_manager.set_qml_property("buildRunCategorization", self._controller.get_build_run_categorization_qml())

    def _create_renderer(self):
        # something is happening here
        # point_cloud_file = "data/360_v2/room/sparse/sparse.ply"
        # point_cloud = PyntCloud.from_file(point_cloud_file)
        # prepare_point_cloud(point_cloud)

        # renderer = PointCloudGLWidget(point_cloud.points)
        renderer = QWidget()
        self._main_view.configure_renderer(renderer)

    def _open_dialog(self):
        dialog = QFileDialog.getExistingDirectoryUrl(self._main_view, "Choose directory", "", QFileDialog.Option.ShowDirsOnly)
        dir_path = QUrl(dialog).toLocalFile()
        self._controller.set_file_list(dir_path)
        
    def _open_progress_bar(self):
        # loading_window = LoadingWindow(self._main_view)
        # loading_window.show()
        pass