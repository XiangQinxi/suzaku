import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)
imm32 = ctypes.WinDLL("imm32", use_last_error=True)

# 类型定义
HWND = wintypes.HWND
HIMC = wintypes.HANDLE
DWORD = wintypes.DWORD
LONG = wintypes.LONG


class POINT(ctypes.Structure):
    _fields_ = [("x", LONG), ("y", LONG)]


class RECT(ctypes.Structure):
    _fields_ = [("left", LONG), ("top", LONG), ("right", LONG), ("bottom", LONG)]


class CANDIDATEFORM(ctypes.Structure):
    _fields_ = [
        ("dwIndex", DWORD),
        ("dwStyle", DWORD),
        ("ptCurrentPos", POINT),
        ("rcArea", RECT),
    ]


# 函数声明
imm32.ImmGetContext.restype = HIMC
imm32.ImmGetContext.argtypes = [HWND]

imm32.ImmReleaseContext.restype = wintypes.BOOL
imm32.ImmReleaseContext.argtypes = [HWND, HIMC]

imm32.ImmSetCandidateWindow.restype = wintypes.BOOL
imm32.ImmSetCandidateWindow.argtypes = [HIMC, ctypes.POINTER(CANDIDATEFORM)]

# 常量
CFS_CANDIDATEPOS = 0x40  # 直接指定候选框位置
CFS_EXCLUDE = 0x80  # 排除区域


def set_candidate_pos(hwnd, x, y):
    himc = imm32.ImmGetContext(hwnd)
    if not himc:
        return False

    form = CANDIDATEFORM()
    form.dwIndex = 0
    form.dwStyle = CFS_CANDIDATEPOS
    form.ptCurrentPos = POINT(x, y)
    form.rcArea = RECT(0, 0, 0, 0)

    ok = imm32.ImmSetCandidateWindow(himc, ctypes.byref(form))
    imm32.ImmReleaseContext(hwnd, himc)
    return bool(ok)


hwnd = user32.GetForegroundWindow()
set_candidate_pos(hwnd, 100, 200)
