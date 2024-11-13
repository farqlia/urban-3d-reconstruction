from PySide6.QtCore import QThreadPool
from ..models.basic_model import BasicModelBool, BasicModelFunc
from ..models.basic_thread import BasicThreadScript

class BuildHandler:
    def __init__(self, script, callback):
        self._script = BasicThreadScript(script, callback)
        self._func = BasicModelFunc(self._exec_script)

    @property
    def func(self):
        return self._func

    def _exec_script(self):
        QThreadPool.globalInstance().start(self._script)