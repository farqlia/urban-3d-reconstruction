from PySide6.QtCore import QThreadPool
from ..models.basic_model import BasicModelBool, BasicModelFunc, BasicModelStr
from ..models.basic_thread import BasicThreadScript

class BuildInfoHandler:
    def __init__(self):
        self._is_build_open = BasicModelBool()
        self._is_build_succ = BasicModelBool()
        self._is_build_fail = BasicModelBool()
        self._build_info = BasicModelStr()
        
    @property
    def is_build_open(self):
        return self._is_build_open

    @property
    def is_build_succ(self):
        return self._is_build_succ

    @property
    def is_build_fail(self):
        return self._is_build_fail
    
    @property
    def build_info(self):
        return self._build_info
    
    def configure_open_handler(self, func):
        self.is_build_open.dataChanged.connect(lambda: self._handle_open(func))

    def _handle_open(self, func):
        if self.is_build_open.data:
            self.is_build_open.data = False
            func()

    def configure_succ_handler(self, func, func2):
        self.is_build_succ.dataChanged.connect(lambda: self._handle_succ(func, func2))
    
    def _handle_succ(self, func, func2):
        if self.is_build_succ.data:
            func()
        else:
            func2()

    def configure_fail_handler(self, func, func2):
        self.is_build_fail.dataChanged.connect(lambda: self._handle_fail(func, func2))

    def _handle_fail(self, func, func2):
        if self.is_build_fail.data:
            func()
        else:
            func2()