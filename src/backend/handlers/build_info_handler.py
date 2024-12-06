from PySide6.QtCore import QThreadPool
from ..models.basic_model import BasicModelBool, BasicModelFunc
from ..models.basic_thread import BasicThreadScript

class BuildInfoHandler:
    def __init__(self):
        self._is_build_open = BasicModelBool()
        self._is_build_succ = BasicModelBool()
        self._is_build_fail = BasicModelBool()
        
    @property
    def is_build_open(self):
        return self._is_build_open

    @property
    def is_build_succ(self):
        return self._is_build_succ

    @property
    def is_build_fail(self):
        return self._is_build_fail
    
    def configure_open_handler(self, func):
        self.is_build_open.dataChanged.connect(lambda: self._handle_open(func))

    def _handle_open(self, func):
        if self.is_build_open.data:
            self.is_build_open.data = False
            func()

    def configure_succ_handler(self, func):
        self.is_build_succ.dataChanged.connect(lambda: self._handle_succ(func))
    
    def _handle_succ(self, func):
        if self.is_build_succ.data:
            self.is_build_succ.data = False
            func()

    def configure_fail_handler(self, func):
        self.is_build_fail.dataChanged.connect(lambda: self._handle_fail(func))

    def _handle_fail(self, func):
        if self.is_build_fail.data:
            self.is_build_fail.data = False
            func()