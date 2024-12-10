from ..models.basic_model import BasicModelBool, BasicModelStr, BasicModelList

class DialogHandler:
    def __init__(self):
        self._is_dialog_open = BasicModelBool()
        self._directory_path = BasicModelStr()
        self._file_list = BasicModelList()
        self._is_file_list_open = BasicModelBool(True)

    @property
    def is_dialog_open(self):
        return self._is_dialog_open

    @property
    def directory_path(self):
        return self._directory_path

    @property
    def file_list(self):
        return self._file_list
    
    @property
    def is_file_list_open(self):
        return self._is_file_list_open

    def configure_handler_is_dialog_open(self, func):
        self.is_dialog_open.dataChanged.connect(lambda: self._handle_is_dialog_open(func))

    def _handle_is_dialog_open(self, func):
        if self.is_dialog_open.data:
            self.is_dialog_open.data = False
            func()
    
    def configure_handler_is_file_list_open(self, func):
        self.is_file_list_open.dataChanged.connect(lambda: self._handle_is_file_list_open(func))
    
    def _handle_is_file_list_open(self, func):
        func()