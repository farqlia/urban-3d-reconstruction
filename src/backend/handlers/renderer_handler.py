from ..models.basic_model import BasicModelBool

class RendererHandler:
    def __init__(self):
        self._is_model = BasicModelBool()

    @property
    def is_model(self):
        return self._is_model

    def configure_handler(self, func):
        self.is_model.dataChanged.connect(lambda: self._handle(func))

    def _handle(self, func):
        if self.is_model.data:
            self.is_model.data = False
            func()