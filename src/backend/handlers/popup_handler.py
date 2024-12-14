from ..models.basic_model import BasicModelBool, BasicModelList

class PopupHandler:
    def __init__(self):
        self._is_popup_open = BasicModelBool()
        self._popup_status = BasicModelBool()

    @property
    def is_popup_open(self):
        return self._is_popup_open

    @property
    def status(self):
        return self._popup_status

    def configure_open_handler(self, func):
        self._is_popup_open.dataChanged.connect(lambda: self._handle_open(func))

    def _handle_open(self, func):
        func()