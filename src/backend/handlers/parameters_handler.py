import os
from ..models.basic_model import BasicModelBool, BasicModelList

class ParametersHandler:
    def __init__(self):
        self._is_parameters_open = BasicModelBool()
        self._status = BasicModelBool()
        self._params = BasicModelList()
        # default
        self._params.data = [
            "default",
            "100000",
            "3000000",
            "100",
            "1"
        ]
    
    @property
    def is_parameters_open(self):
        return self._is_parameters_open

    @property
    def status(self):
        return self._status
    
    @property
    def params(self):
        return self._params

    def configure_open_handler(self, func):
        self.is_parameters_open.dataChanged.connect(lambda: self._handle_open(func))
    
    def configure_status_handler(self, func):
        self.status.dataChanged.connect(lambda: self._handle_status(func))

    def _handle_open(self, func):
        if self.is_parameters_open.data:
            self.is_parameters_open.data = False
            func()
        
    def _handle_status(self, func):
        if self.status.data:
            self.status.data = False
            func()