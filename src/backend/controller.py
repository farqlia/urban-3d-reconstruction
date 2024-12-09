import os
from .handlers.build_handler import BuildHandler
from .handlers.dialog_handler import DialogHandler
from .handlers.tab_handler import TabHandler
from .handlers.renderer_handler import RendererHandler
from .handlers.build_info_handler import BuildInfoHandler
from .handlers.parameters_handler import ParametersHandler
from .handlers.settings_handler import SettingsHandler
from src.urb3d.pipeline.config import INPUT_DATA_FOLDER, DATA_FOLDER, COLMAP_RECONSTRUCTION_DIR, GAUSSIAN_MODEL_PLY, GAUSSIAN_MODEL_PT

class Controller:
    def __init__(self, backend):
        self.backend = backend
        self._build_info_handler = BuildInfoHandler()
        self._settings_handler = SettingsHandler()
        self._point_cloud_build_handler = BuildHandler(backend.reconstruct_point_cloud, lambda x: self.complete_build(x, "reconstruction"))
        self._splats_build_handler = BuildHandler(lambda: backend.create_gaussian_model(
            self._settings_handler.params.data[0],
            int(self._settings_handler.params.data[1]),
            int(self._settings_handler.params.data[2]),
            int(self._settings_handler.params.data[3]),
            int(self._settings_handler.params.data[4])
            ), lambda x: self.complete_build(x, "rendering"))
        self._categorization_handler = BuildHandler(backend.run_segmentation, lambda x: self.complete_build(x, "segmentation"))
        # self._point_cloud_build_handler = BuildHandler(None, lambda x: self.complete_build(x, "reconstruction"))
        # self._splats_build_handler = BuildHandler(None, lambda x: self.complete_build(x, "rendering"))
        # self._categorization_handler = BuildHandler(None, lambda x: self.complete_build(x, "segmentation"))
        self._dialog_handler = DialogHandler()
        self._tab_handler = TabHandler()
        self._renderer_handler = RendererHandler()
        self.viz_type = None
        self._parameters_handler = ParametersHandler()

    def complete_build(self, info, handler):

        # if info is not None: # idk, if something returns then error
          #   self._build_info_handler.is_build_succ.data = True
        # else:
          #   self._build_info_handler.is_build_fail.data = True

        self.viz_type = handler
        self._renderer_handler.is_model.data = True


    def cancel_build(self, info):
        self._build_info_handler.is_build_fail.data = True
        print(info)

    def configure_dialog_open_handler(self, func):
        self._dialog_handler.configure_handler_is_dialog_open(func)
    
    def configure_dialog_file_list_open_handler(self, func):
        self._dialog_handler.configure_handler_is_file_list_open(func)
    
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

    def configure_parameters_handler(self, func):
        self._parameters_handler.configure_open_handler(func)

    def configure_settings_status_handler(self, func):
        n, v = self._dynamic_var_setter(INPUT_DATA_FOLDER)
        self._settings_handler.configure_env_var(n, v)
        n, v = self._dynamic_var_setter(DATA_FOLDER)
        self._settings_handler.configure_env_var(n, v)
        n, v = self._dynamic_var_setter(COLMAP_RECONSTRUCTION_DIR)
        self._settings_handler.configure_env_var(n, v)
        n, v = self._dynamic_var_setter(GAUSSIAN_MODEL_PLY)
        self._settings_handler.configure_env_var(n, v)
        n, v = self._dynamic_var_setter(GAUSSIAN_MODEL_PT)
        self._settings_handler.configure_env_var(n, v)
        self._settings_handler.configure_status_handler(func)
    
    def configure_parameters_status_handler(self, func):
        self._parameters_handler.configure_status_handler(func)

    def get_file_list_qml(self):
        return self._dialog_handler.file_list
    
    def get_is_dialog_open_qml(self):
        return self._dialog_handler.is_dialog_open

    def get_is_file_list_open_qml(self):
        return self._dialog_handler.is_file_list_open

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
    
    def get_is_parameters_open_qml(self):
        return self._parameters_handler.is_parameters_open

    def get_status_settings_open_qml(self):
        return self._settings_handler.status
    
    def get_status_parameters_open_qml(self):
        return self._parameters_handler.status

    def get_vars_settings_open_qml(self):
        return self._settings_handler.env_vars
    
    def get_params_qml(self):
        return self._parameters_handler.params

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
            self.backend.upload_image_folder(dir_path)
    
    def _dynamic_var_setter(self, var):
        for name, value in globals().items():
            if value is var:
                return name, str(var)