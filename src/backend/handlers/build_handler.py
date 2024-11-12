from PySide6.QtCore import QThreadPool
from ..models.basic_model import BasicModelBool, BasicModelFunc
from ..models.basic_thread import BasicThreadScript

class BuildHandler:
    def __init__(self, script, callback):
        self._is_build_open = BasicModelBool()
        self._script = BasicThreadScript(script, callback)
        self._func = BasicModelFunc(self._exec_script)

    @property
    def is_build_open(self):
        return self._is_build_open

    @property
    def func(self):
        return self._func

    def configure_handler(self, func):
        self.is_build_open.dataChanged.connect(lambda: self._handle(func))

    def _handle(self, func):
        if self.is_build_open:
            # self.is_build_open.data = False
            func()

    def _exec_script(self):
        self.is_build_open.data = True
        QThreadPool.globalInstance().start(self._script)