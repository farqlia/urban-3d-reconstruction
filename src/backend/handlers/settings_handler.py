from ..models.basic_model import BasicModelBool

class SettingsHandler:
    def __init__(self):
        self._is_settings_open = BasicModelBool()
    
    @property
    def is_settings_open(self):
        return self._is_settings_open

    def configure_handler(self, func):
        self.is_settings_open.dataChanged.connect(lambda: self._handle(func))

    def _handle(self, func):
        if self.is_settings_open.data:
            self.is_settings_open.data = False
            func()