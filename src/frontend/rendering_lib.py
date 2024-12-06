import ctypes
import platform

def get_rendering_lib():
    RENDERING_LIB = "src/rendering/rendering_lib"

    os_name = platform.system()

    if os_name == "Linux":
        RENDERING_LIB += ".so"
    else:
        RENDERING_LIB += ".dll"

    lib = ctypes.CDLL(RENDERING_LIB)
    
    lib.initWindow.restype = None
    lib.loadData.restype = None
    lib.loadData.argtypes = [ctypes.c_char_p]
    lib.getWindowId.restype = ctypes.c_long
    lib.run.restype = None
    lib.close.restype = None
    lib.cleanUp.restype = None

    return lib
