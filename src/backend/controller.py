import os
from .handlers.build_handler import BuildHandler
from .handlers.dialog_handler import DialogHandler
from .handlers.tab_handler import TabHandler
from .handlers.renderer_handler import RendererHandler
from .handlers.build_info_handler import BuildInfoHandler
from .handlers.settings_handler import SettingsHandler
from src.urb3d.config import INPUT_DATA_FOLDER, DATA_FOLDER, SCENE_FOLDER, GAUSSIAN_MODEL_PLY, GAUSSIAN_MODEL_PT

class Controller:
    def __init__(self, backend):
        self._build_info_handler = BuildInfoHandler()
        self._point_cloud_build_handler = BuildHandler(backend._reconstruct_point_cloud, self.complete_build)
        self._splats_build_handler = BuildHandler(backend._create_gaussian_model, self.complete_build)
        self._categorization_handler = BuildHandler(backend._segment, self.complete_build)
        self._dialog_handler = DialogHandler()
        self._tab_handler = TabHandler()
        self._renderer_handler = RendererHandler()
        self._settings_handler = SettingsHandler()
        self.ply_path = backend.gaussian_ply_path
        self.backend = backend

    def complete_build(self, info):
        if info is not None: # idk, if something returns then error
            self._build_info_handler.is_build_succ.data = True
        else:
            self._build_info_handler.is_build_fail.data = True
        self._renderer_handler.is_model.data = True
        self.ply_path = self.backend.gaussian_ply_path
        print(info)

    def cancel_build(self, info):
        self._build_info_handler.is_build_fail.data = True
        print(info)

    def configure_dialog_handler(self, func):
        self._dialog_handler.configure_handler(func)
    
    def configure_open_build_run_handler(self, func):
        self._build_info_handler.configure_open_handler(func)

    def configure_succ_build_run_handler(self, func):
        self._build_info_handler.configure_succ_handler(func)

    def configure_fail_build_run_handler(self, func):
        self._build_info_handler.configure_fail_handler(func)

    def configure_renderer_handler(self, func):
        self._renderer_handler.configure_handler(func)

    def configure_settings_handler(self, func):
        self._settings_handler.configure_open_handler(func)

    def configure_settings_status_handler(self, func):
        n, v = self._dynamic_var_setter(INPUT_DATA_FOLDER)
        self._settings_handler.configure_env_var(n, v)
        n, v = self._dynamic_var_setter(DATA_FOLDER)
        self._settings_handler.configure_env_var(n, v)
        n, v = self._dynamic_var_setter(SCENE_FOLDER)
        self._settings_handler.configure_env_var(n, v)
        n, v = self._dynamic_var_setter(GAUSSIAN_MODEL_PLY)
        self._settings_handler.configure_env_var(n, v)
        n, v = self._dynamic_var_setter(GAUSSIAN_MODEL_PT)
        self._settings_handler.configure_env_var(n, v)
        self._settings_handler.configure_status_handler(func)

    def get_file_list_qml(self):
        return self._dialog_handler.file_list
    
    def get_is_dialog_open_qml(self):
        return self._dialog_handler.is_dialog_open

    def get_selected_tab_qml(self):
        return self._tab_handler.selected_tab

    def get_is_build_open_qml(self):
        return self._build_info_handler.is_build_open

    def get_is_build_succ_qml(self):
        return self._build_info_handler.is_build_succ

    def get_is_build_fail_qml(self):
        return self._build_info_handler.is_build_fail

    def get_is_settings_open_qml(self):
        return self._settings_handler.is_settings_open

    def get_status_settings_open_qml(self):
        return self._settings_handler.status

    def get_vars_settings_open_qml(self):
        return self._settings_handler.env_vars

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
    
    def _dynamic_var_setter(self, var):
        for name, value in globals().items():
            if value is var:
                return name, str(var)