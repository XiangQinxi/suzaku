import ctypes as ct
from ctypes import wintypes as w

SPI_GETDESKWALLPAPER = 0x0073

dll = ct.WinDLL('user32')
dll.SystemParametersInfoW.argtypes = w.UINT,w.UINT,w.LPVOID,w.UINT
dll.SystemParametersInfoW.restype = w.BOOL

path = ct.create_unicode_buffer(260)
result = dll.SystemParametersInfoW(SPI_GETDESKWALLPAPER, ct.sizeof(path), path, 0)
print(result, path.value)