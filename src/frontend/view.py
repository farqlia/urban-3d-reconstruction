from pyntcloud import PyntCloud

from src.urb3d.pipeline.config import TEST_MODEL_PLY_PATH, GAUSSIAN_MODEL_PLY, POINT_CLOUD_SPARSE, FILTERED_PRESEG_MODEL, PNG_RENDERS_FOLDER, COLORED_SEGMENTED_PLY_PATH
from src.urb3d.rendering.render_point_cloud import PointCloudWidget, prepare_point_cloud
from src.urb3d.rendering.slideshow import SlideshowWidget
from .view_engine_manager import EngineManager
from .views.main_window import MainWindow

import os
from PySide6.QtCore import QObject, QUrl, Qt, QThreadPool
from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtQuick import QQuickWindow, QSGRendererInterface
from PySide6.QtQuickWidgets import QQuickWidget

from src.backend.models.basic_thread import BasicThreadScript
from .config import LOADING_WINDOW_FILE, FAIL_WINDOW_FILE, SUCC_WINDOW_FILE, SETTINGS_WINDOW, PARAMETERS_WINDOW
from .external_window import external_window
from .views.sliding_widget import SlidingWidget

class View:
    def __init__(self, controller, lib):
        QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)
        self._controller = controller
        self._engine_manager = EngineManager()
        self.rendering_lib = lib
        self._configure_engine_properties()
        self._configure_handlers()
        self.popup_on = False
        self.lib_init = False

        self._main_view = MainWindow(self, self._engine_manager, self.rendering_lib)
        self._loading_window = None

    def run(self):
        self._create_renderer()
        self._main_view.show()

    def _configure_handlers(self):
        self._controller.configure_dialog_open_handler(self.open_dialog)
        self._controller.configure_dialog_file_list_open_handler(self.wrapper_slidig_widget)
        self._controller.configure_open_build_run_handler(self.build)
        self._controller.configure_succ_build_run_handler(self.build_succ, self.close_popup_window)
        self._controller.configure_fail_build_run_handler(self.build_fail, self.close_popup_window)
        self._controller.configure_renderer_handler(self._create_renderer)
        self._controller.configure_settings_handler(lambda: self.open_popup_window(SETTINGS_WINDOW))
        self._controller.configure_settings_status_handler(self.close_popup_window)
        self._controller.configure_parameters_handler(lambda: self.open_popup_window(PARAMETERS_WINDOW))
        self._controller.configure_parameters_status_handler(self.close_popup_window)

    def _configure_engine_properties(self):
        self._engine_manager.set_qml_property("fileList", self._controller.get_file_list_qml())
        self._engine_manager.set_qml_property("selectedTab", self._controller.get_selected_tab_qml())
        self._engine_manager.set_qml_property("isDialogOpen", self._controller.get_is_dialog_open_qml())
        self._engine_manager.set_qml_property("isFileListOpen", self._controller.get_is_file_list_open_qml())
        self._engine_manager.set_qml_property("isBuildOpen", self._controller.get_is_build_open_qml())
        self._engine_manager.set_qml_property("isBuildSucc", self._controller.get_is_build_succ_qml())
        self._engine_manager.set_qml_property("isBuildFail", self._controller.get_is_build_fail_qml())
        self._engine_manager.set_qml_property("isSettingsOpen", self._controller.get_is_settings_open_qml())
        self._engine_manager.set_qml_property("settingsStatus", self._controller.get_status_settings_open_qml())
        self._engine_manager.set_qml_property("settingsVars", self._controller.get_vars_settings_open_qml())
        self._engine_manager.set_qml_property("renderingType", self._controller.get_rendering_settings_open_qml())
        self._engine_manager.set_qml_property("isParametersOpen", self._controller.get_is_parameters_open_qml())
        self._engine_manager.set_qml_property("parametersStatus", self._controller.get_status_parameters_open_qml())
        self._engine_manager.set_qml_property("parametersVars", self._controller.get_params_qml())
        self._engine_manager.set_qml_property("buildRunCloud", self._controller.get_build_run_cloud_qml())
        self._engine_manager.set_qml_property("buildRunSplats", self._controller.get_build_run_splats_qml())
        self._engine_manager.set_qml_property("buildRunCategorization", self._controller.get_build_run_categorization_qml())
        self._engine_manager.set_qml_property("buildInfo", self._controller.get_build_info())

    def _create_renderer(self):
        self.renderer = None

        if (self.lib_init):
            self.rendering_lib.close()
            self.rendering_lib.cleanUp()
            self.lib_init = False

        # cloud_file = "data/tester2.ply"

        if self._controller.viz_type == "reconstruction":
            cloud_file = str(FILTERED_PRESEG_MODEL) if FILTERED_PRESEG_MODEL.exists() else str(POINT_CLOUD_SPARSE)
            # cloud_file = str(TEST_MODEL_PLY_PATH)

            if self._controller.rendering_type == 1:
                thread_pool = QThreadPool.globalInstance()

                def bundle():
                    self.rendering_lib.initWindow()
                    window_id = self.rendering_lib.getWindowId()
                    self.renderer = external_window(window_id)
                    print("Loading shader data")
                    self.rendering_lib.loadData(cloud_file.encode('utf-8'))
                    print("Done loading shader data")
                    self.rendering_lib.run()

                thread_pool.start(BasicThreadScript(bundle, lambda x: None))

                while(self.renderer is None):
                    continue

                self.lib_init = True

                # self.renderer.moveToThread(self._main_view.thread())
                # self.renderer = QWidget.createWindowContainer(self.renderer)
            else:
                cloud_file = str(FILTERED_PRESEG_MODEL) if FILTERED_PRESEG_MODEL.exists() else str(POINT_CLOUD_SPARSE)
                pc = PyntCloud.from_file(cloud_file)
                prepare_point_cloud(pc, flip=False, normalize_colors=cloud_file == str(POINT_CLOUD_SPARSE))
                self.renderer = PointCloudWidget(pc)

        elif self._controller.viz_type == "rendering":
            self.renderer = SlideshowWidget(PNG_RENDERS_FOLDER)

        elif self._controller.viz_type == "segmentation":
            pc = PyntCloud.from_file(str(COLORED_SEGMENTED_PLY_PATH))
            prepare_point_cloud(pc, flip=False, normalize_colors=True)
            self.renderer = PointCloudWidget(pc)

        if self.renderer is not None:
            print("Configure renderer")
            self._main_view.configure_renderer(self.renderer)

    def open_dialog(self):
        dialog = QFileDialog.getExistingDirectoryUrl(self._main_view, "Choose directory", "", QFileDialog.Option.ShowDirsOnly)
        dir_path = QUrl(dialog).toLocalFile()
        self._controller.set_file_list(dir_path)

    def build(self):
        self.open_popup_window(LOADING_WINDOW_FILE)

    def build_succ(self):
        self.close_popup_window()
        self.open_popup_window(SUCC_WINDOW_FILE)
        
    def build_fail(self):
        self.close_popup_window()
        self.open_popup_window(FAIL_WINDOW_FILE)
    
    def open_popup_window(self, component):
        if self.popup_on:
            return

        self.popup = self._engine_manager.load_component(component, self._main_view)
        parent_rect = self._main_view.rect()
        self.popup.setGeometry(
            (parent_rect.width() - self.popup.width()) // 2,
            (parent_rect.height() - self.popup.height()) // 2,
            self.popup.width(),
            self.popup.height()
        )
        self.popup.show()
        self.popup_on = True

    def close_popup_window(self):
        if self.popup is not None:
            self.popup.hide()
            self.popup.deleteLater()
            self.popup_on = False

    def wrapper_slidig_widget(self):
        self._main_view.slide_body()

    def _reload(self):
        # write something to refresh ui after .env changes inside program
        pass