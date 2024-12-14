import ctypes
import os
import platform
from pathlib import Path

class RenderingLibrary:
    def __init__(self):
        lib_path = Path(r"C:\Users\julia\PycharmProjects\urb3drecon\src\urb3d\rendering")

        self._lib = None
        # os.environ["WINEPREFIX"] = "/home/frafau/.wine"

        if platform.system() == "Linux":
            lib_path += "librendering_lib.so"
            self._lib = ctypes.CDLL(lib_path)
        else:
            lib_path = str(lib_path / "librendering_lib.dll")
            self._lib = ctypes.WinDLL(lib_path)
        
        self._lib.initWindow.restype = None
        self._lib.loadData.restype = None
        self._lib.loadData.argtypes = [ctypes.c_char_p]
        self._lib.getWindowId.restype = ctypes.c_long
        self._lib.run.restype = None
        self._lib.close.restype = None
        self._lib.cleanUp.restype = None
    
    @property
    def lib(self):
        return self._lib