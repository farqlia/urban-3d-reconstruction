from ..models.basic_model import BasicModelBool, BasicModelStr, BasicModelList

class DialogHandler:
    def __init__(self):
        self._is_open_dialog = BasicModelBool()
        self._directory_path = BasicModelStr()
        self._file_list = BasicModelList()

    @property
    def is_open_dialog(self):
        return self._is_open_dialog

    @property
    def directory_path(self):
        return self._directory_path

    @property
    def file_list(self):
        return self._file_list

    def configure_handler(self, func):
        self.is_open_dialog.dataChanged.connect(lambda: self._handle(func))

    def _handle(self, func):
        if self.is_open_dialog.data:
            self.is_open_dialog.data = False
            func()