from ..models.basic_model import BasicModelBool, BasicModelStr, BasicModelList

class DialogHandler:
    def __init__(self):
        self._is_dialog_open = BasicModelBool()
        self._directory_path = BasicModelStr()
        self._file_list = BasicModelList()

    @property
    def is_dialog_open(self):
        return self._is_dialog_open

    @property
    def directory_path(self):
        return self._directory_path

    @property
    def file_list(self):
        return self._file_list

    def configure_handler(self, func):
        self.is_dialog_open.dataChanged.connect(lambda: self._handle(func))

    def _handle(self, func):
        if self.is_dialog_open.data:
            self.is_dialog_open.data = False
            func()