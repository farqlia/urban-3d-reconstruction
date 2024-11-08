from PySide6.QtCore import QThread, Signal, QRunnable, QObject
import time

class BasicThreadScript(QRunnable):
    def __init__(self, func, callback, script_path,  *args):
        super().__init__()
        self._script_path = script_path
        self._args = args
        self._func = func
        self._callback = callback

    def run(self):
        result = self._func(self._script_path, *self._args)
        self._callback(result)