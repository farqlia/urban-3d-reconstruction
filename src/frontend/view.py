import os
from PySide6.QtCore import QObject, QUrl, Qt
from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtQuickWidgets import QQuickWidget
from pyntcloud import PyntCloud

from .config import LOADING_WINDOW_FILE
from src.pipeline.config import DATA_FOLDER
from .views.main_window import MainWindow
from .views.loading_window import LoadingWindow
from .view_engine_manager import EngineManager
from src.rendering.render_point_cloud import PointCloudGLWidget, prepare_point_cloud

class View:
    def __init__(self, controller):
        QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)
        self._controller = controller
        self._engine_manager = EngineManager()
        self._configure_engine_properties()
        self._configure_handlers()

        self._main_view = MainWindow(self._engine_manager)

    def run(self):
        # self._create_renderer()
        self._main_view.show()

    def _configure_handlers(self):
        self._controller.configure_dialog_handler(self._open_dialog)
        self._controller.configure_open_build_run_handler(self._open_progress_bar)
        self._controller.configure_succ_build_run_handler(self._close_progress_bar)
        self._controller.configure_fail_build_run_handler(self._close_progress_bar)
        self._controller.configure_renderer_handler(self._create_renderer)
        self._controller.configure_settings_handler(self._open_progress_bar)

    def _configure_engine_properties(self):
        self._engine_manager.set_qml_property("fileList", self._controller.get_file_list_qml())
        self._engine_manager.set_qml_property("selectedTab", self._controller.get_selected_tab_qml())
        self._engine_manager.set_qml_property("isDialogOpen", self._controller.get_is_dialog_open_qml())
        self._engine_manager.set_qml_property("isBuildOpen", self._controller.get_is_build_open_qml())
        self._engine_manager.set_qml_property("isBuildSucc", self._controller.get_is_build_succ_qml())
        self._engine_manager.set_qml_property("isBuildFail", self._controller.get_is_build_fail_qml())
        self._engine_manager.set_qml_property("isSettingsOpen", self._controller.get_is_settings_open_qml())
        self._engine_manager.set_qml_property("buildRunCloud", self._controller.get_build_run_cloud_qml())
        self._engine_manager.set_qml_property("buildRunSplats", self._controller.get_build_run_splats_qml())
        self._engine_manager.set_qml_property("buildRunCategorization", self._controller.get_build_run_categorization_qml())

    def _create_renderer(self):
        # something is happening here
        renderer = None

        pc_file = str(DATA_FOLDER) + "/sparse.ply"
        if (os.path.exists(pc_file)):
            pc = PyntCloud.from_file(pc_file)
            prepare_point_cloud(pc)
            renderer = PointCloudGLWidget(pc.points)
        
        if renderer is None:
            renderer = QWidget()

        self._main_view.configure_renderer(renderer)

    def _open_dialog(self):
        dialog = QFileDialog.getExistingDirectoryUrl(self._main_view, "Choose directory", "", QFileDialog.Option.ShowDirsOnly)
        dir_path = QUrl(dialog).toLocalFile()
        self._controller.set_file_list(dir_path)
        
    def _open_progress_bar(self):
        self._loading_window = self._engine_manager.load_component(LOADING_WINDOW_FILE, self._main_view)
        parent_rect = self._main_view.rect()
        self._loading_window.setGeometry(
            (parent_rect.width() - self._loading_window.width()) // 2,
            (parent_rect.height() - self._loading_window.height()) // 2,
            self._loading_window.width(),
            self._loading_window.height()
        )
        self._loading_window.show()
    
    def _close_progress_bar(self):
        self._loading_window.hide()
        # self._loading_window.setParent(None)
        self._loading_window.deleteLater()

    def _open_succ_window(self):
        pass

    def _open_fail_window(self):
        pass