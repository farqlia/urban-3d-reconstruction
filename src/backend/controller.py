import os
from .handlers.build_handler import BuildHandler
from .handlers.dialog_handler import DialogHandler
from .handlers.tab_handler import TabHandler

class Controller:
    def __init__(self, backend):
        self._point_cloud_build_handler = BuildHandler(backend._reconstruct_point_cloud, self.cancel_build)
        self._splats_build_handler = BuildHandler(backend._create_gaussian_model, self.cancel_build)
        self._categorization_handler = BuildHandler(lambda: None, lambda: None)
        self._dialog_handler = DialogHandler()
        self._tab_handler = TabHandler()

    def cancel_build(self, info):
        self._point_cloud_build_handler.is_build_open.data = False
        self._splats_build_handler.is_build_open.data = False
        self._categorization_handler.is_build_open.data = False
        print(info)

    def configure_dialog_handler(self, func):
        self._dialog_handler.configure_handler(func)
    
    def configure_build_run_handler(self, func):
        self._point_cloud_build_handler.configure_handler(func)
        self._splats_build_handler.configure_handler(func)
        self._categorization_handler.configure_handler(func)

    def get_file_list_qml(self):
        return self._dialog_handler.file_list
    
    def get_is_dialog_open_qml(self):
        return self._dialog_handler.is_open_dialog

    def get_selected_tab_qml(self):
        return self._tab_handler.selected_tab

    def get_build_run_cloud_qml(self):
        return self._point_cloud_build_handler.func

    def get_build_run_splats_qml(self):
        return self._splats_build_handler.func

    def get_build_run_categorization_qml(self):
        return self._categorization_handler.func

    def set_file_list(self, dir_path):
        if dir_path:
            self._dialog_handler.file_list.data = [f for f in  os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
            self._dialog_handler.directory_path.data = dir_path
            os.environ["INPUT_DATA_FOLDER"] = dir_path

