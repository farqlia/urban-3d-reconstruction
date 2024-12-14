from PySide6.QtCore import QThreadPool
from ..models.basic_model import BasicModelBool, BasicModelFunc
from ..models.basic_thread import BasicThreadScript

class BuildHandler:
    def __init__(self, script, callback):
        self._script = script
        self._callback = callback
        self._func = BasicModelFunc(self._exec_script)

    @property
    def func(self):
        return self._func

    def _exec_script(self):
        script = BasicThreadScript(self._script, self._callback)
        QThreadPool.globalInstance().start(script)