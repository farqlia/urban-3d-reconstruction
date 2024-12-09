from PySide6.QtCore import QUrl
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtWidgets import QFileDialog
from pyntcloud import PyntCloud

from urb3d.pipeline.config import GAUSSIAN_MODEL_PLY, POINT_CLOUD_SPARSE, FILTERED_PRESEG_MODEL, PNG_RENDERS_FOLDER, COLORED_SEGMENTED_PLY_PATH
from urb3d.rendering.render_point_cloud import PointCloudWidget, prepare_point_cloud
from urb3d.rendering.slideshow import SlideshowWidget
from .config import LOADING_WINDOW_FILE, FAIL_WINDOW_FILE, SUCC_WINDOW_FILE, SETTINGS_WINDOW
from .view_engine_manager import EngineManager
from .views.main_window import MainWindow


class View:
    def __init__(self, controller):
        QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)
        self._controller = controller
        self._engine_manager = EngineManager()
        self._configure_engine_properties()
        self._configure_handlers()

        self._main_view = MainWindow(self._engine_manager)
        self._loading_window = None

    def run(self):
        self._create_renderer()
        self._main_view.show()

    def _configure_handlers(self):
        self._controller.configure_dialog_handler(self._open_dialog)
        self._controller.configure_open_build_run_handler(self._build)
        self._controller.configure_succ_build_run_handler(self._build_succ)
        self._controller.configure_fail_build_run_handler(self._build_fail)
        self._controller.configure_renderer_handler(self._create_renderer)
        self._controller.configure_settings_handler(self._open_settings_window)
        self._controller.configure_settings_status_handler(self._close_settings_window)

    def _configure_engine_properties(self):
        self._engine_manager.set_qml_property("fileList", self._controller.get_file_list_qml())
        self._engine_manager.set_qml_property("selectedTab", self._controller.get_selected_tab_qml())
        self._engine_manager.set_qml_property("isDialogOpen", self._controller.get_is_dialog_open_qml())
        self._engine_manager.set_qml_property("isBuildOpen", self._controller.get_is_build_open_qml())
        self._engine_manager.set_qml_property("isBuildSucc", self._controller.get_is_build_succ_qml())
        self._engine_manager.set_qml_property("isBuildFail", self._controller.get_is_build_fail_qml())
        self._engine_manager.set_qml_property("isSettingsOpen", self._controller.get_is_settings_open_qml())
        self._engine_manager.set_qml_property("settingsStatus", self._controller.get_status_settings_open_qml())
        self._engine_manager.set_qml_property("settingsVars", self._controller.get_vars_settings_open_qml())
        self._engine_manager.set_qml_property("buildRunCloud", self._controller.get_build_run_cloud_qml())
        self._engine_manager.set_qml_property("buildRunSplats", self._controller.get_build_run_splats_qml())
        self._engine_manager.set_qml_property("buildRunCategorization", self._controller.get_build_run_categorization_qml())
        self._engine_manager.set_qml_property("backend", self._controller.get_backend_qml())

    def _create_renderer(self):

        print(self._controller.viz_type)

        renderer = None

        if self._controller.viz_type == "reconstruction":
            cloud_file = str(FILTERED_PRESEG_MODEL) if FILTERED_PRESEG_MODEL.exists() else str(POINT_CLOUD_SPARSE)
            pc = PyntCloud.from_file(cloud_file)
            prepare_point_cloud(pc, flip=False, normalize_colors=cloud_file == str(POINT_CLOUD_SPARSE))
            renderer = PointCloudWidget(pc)

        elif self._controller.viz_type == "rendering":
            renderer = SlideshowWidget(PNG_RENDERS_FOLDER)

        elif self._controller.viz_type == "segmentation":
            pc = PyntCloud.from_file(str(COLORED_SEGMENTED_PLY_PATH))
            prepare_point_cloud(pc, flip=False, normalize_colors=True)
            renderer = PointCloudWidget(pc)

        if renderer is not None:
            print("Configure renderer")
            self._main_view.configure_renderer(renderer, self._controller.viz_type)


    def _open_dialog(self):
        dialog = QFileDialog.getExistingDirectoryUrl(self._main_view, "Choose directory", "", QFileDialog.Option.ShowDirsOnly)
        dir_path = QUrl(dialog).toLocalFile()
        self._controller.set_file_list(dir_path)

    def _build(self):
        self._open_progress_bar()

    def _build_succ(self):
        self._close_progress_bar()
        self._open_succ_window()

    def _build_fail(self):
        self._close_progress_bar()
        self._open_fail_window()

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
        if self._loading_window is not None:
            self._loading_window.hide()
            self._loading_window.deleteLater()
    
    def _open_succ_window(self):
        self._succ_window = self._engine_manager.load_component(SUCC_WINDOW_FILE, self._main_view)
        parent_rect = self._main_view.rect()
        self._succ_window.setGeometry(
            (parent_rect.width() - self._succ_window.width()) // 2,
            (parent_rect.height() - self._succ_window.height()) // 2,
            self._succ_window.width(),
            self._succ_window.height()
        )
        self._succ_window.show()

    def _close_fail_window(self):
        if self._succ_window is not None:
            self._succ_window.hide()
            self._succ_window.deleteLater()

    def _open_fail_window(self):
        self._fail_window = self._engine_manager.load_component(FAIL_WINDOW_FILE, self._main_view)
        parent_rect = self._main_view.rect()
        self._fail_window.setGeometry(
            (parent_rect.width() - self._fail_window.width()) // 2,
            (parent_rect.height() - self._fail_window.height()) // 2,
            self._fail_window.width(),
            self._fail_window.height()
        )
        self._fail_window.show()

    def _close_fail_window(self):
        if self._fail_window is not None:
            self._fail_window.hide()
            self._fail_window.deleteLater()

    def _open_settings_window(self):
        self._settings_window = self._engine_manager.load_component(SETTINGS_WINDOW, self._main_view)
        parent_rect = self._main_view.rect()
        self._settings_window.setGeometry(
            (parent_rect.width() - self._settings_window.width()) // 2,
            (parent_rect.height() - self._settings_window.height()) // 2,
            self._settings_window.width(),
            self._settings_window.height()
        )
        self._settings_window.show()

    def _close_settings_window(self):
        if self._settings_window is not None:
            self._settings_window.hide()
            self._settings_window.deleteLater()

    def _reload(self):
        # write something to refresh ui after .env changes inside program
        pass