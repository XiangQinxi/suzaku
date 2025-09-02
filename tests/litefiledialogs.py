"""
LiteFileDialog — 精简跨平台文件/文件夹对话框

目标：
- Windows 平台：使用 ctypes 调用 GetOpenFileNameW / GetSaveFileNameW / SHBrowseForFolder（无 pywin32 依赖）。
- 其他平台：使用 filedialpy 库（第三方，需要 pip 安装）。

API：open_file / save_file / select_folder

返回值：
- open_file(..., multiple=True) -> list[str] 或 None
- open_file(..., multiple=False) -> str 或 None
- save_file(...) -> str 或 None
- select_folder(...) -> str 或 None

"""

from __future__ import annotations

import os
import platform
from typing import Optional, Sequence, Tuple

FileTypes = Sequence[
    Tuple[str, str]
]  # [(label, pattern)]，如 [("Images", "*.png *.jpg")]

# ------------------------------
# Windows ctypes 实现
# ------------------------------
if os.name == "nt":
    import ctypes
    from ctypes import wintypes

    class OPENFILENAMEW(ctypes.Structure):
        _fields_ = [
            ("lStructSize", wintypes.DWORD),
            ("hwndOwner", wintypes.HWND),
            ("hInstance", wintypes.HINSTANCE),
            ("lpstrFilter", wintypes.LPCWSTR),
            ("lpstrCustomFilter", wintypes.LPWSTR),
            ("nMaxCustFilter", wintypes.DWORD),
            ("nFilterIndex", wintypes.DWORD),
            ("lpstrFile", wintypes.LPWSTR),
            ("nMaxFile", wintypes.DWORD),
            ("lpstrFileTitle", wintypes.LPWSTR),
            ("nMaxFileTitle", wintypes.DWORD),
            ("lpstrInitialDir", wintypes.LPCWSTR),
            ("lpstrTitle", wintypes.LPCWSTR),
            ("Flags", wintypes.DWORD),
            ("nFileOffset", wintypes.WORD),
            ("nFileExtension", wintypes.WORD),
            ("lpstrDefExt", wintypes.LPCWSTR),
            ("lCustData", wintypes.LPARAM),
            ("lpfnHook", wintypes.LPVOID),
            ("lpTemplateName", wintypes.LPCWSTR),
            ("pvReserved", wintypes.LPVOID),
            ("dwReserved", wintypes.DWORD),
            ("FlagsEx", wintypes.DWORD),
        ]

    comdlg32 = ctypes.WinDLL("comdlg32", use_last_error=True)
    shell32 = ctypes.WinDLL("shell32", use_last_error=True)

    OFN_EXPLORER = 0x00080000
    OFN_FILEMUSTEXIST = 0x00001000
    OFN_PATHMUSTEXIST = 0x00000800
    OFN_ALLOWMULTISELECT = 0x00000200
    OFN_HIDEREADONLY = 0x00000004
    OFN_OVERWRITEPROMPT = 0x00000002

    BIF_RETURNONLYFSDIRS = 0x00000001
    BIF_NEWDIALOGSTYLE = 0x00000040

    class BROWSEINFO(ctypes.Structure):
        _fields_ = [
            ("hwndOwner", wintypes.HWND),
            ("pidlRoot", wintypes.LPVOID),
            ("pszDisplayName", wintypes.LPWSTR),
            ("lpszTitle", wintypes.LPCWSTR),
            ("ulFlags", wintypes.UINT),
            ("lpfn", wintypes.LPVOID),
            ("lParam", wintypes.LPARAM),
            ("iImage", wintypes.INT),
        ]

    SHBrowseForFolderW = shell32.SHBrowseForFolderW
    SHGetPathFromIDListW = shell32.SHGetPathFromIDListW

    def _win_build_filter(filetypes: Optional[FileTypes]) -> str:
        if not filetypes:
            return "All files\0*.*\0\0"
        parts = []
        for label, patt in filetypes:
            parts.append(label)
            parts.append(patt)
        parts.append("All files")
        parts.append("*.*")
        return "\0".join(parts) + "\0\0"

    def _win_open_file(
        title: str,
        initialdir: Optional[str],
        filetypes: Optional[FileTypes],
        defaultextension: Optional[str],
        multiple: bool,
    ):
        buf_size = 65536 if multiple else 4096
        file_buffer = ctypes.create_unicode_buffer(buf_size)
        ofn = OPENFILENAMEW()
        ofn.lStructSize = ctypes.sizeof(OPENFILENAMEW)
        ofn.lpstrFilter = _win_build_filter(filetypes)
        ofn.nFilterIndex = 1
        ofn.lpstrFile = ctypes.cast(file_buffer, wintypes.LPWSTR)
        ofn.nMaxFile = buf_size
        ofn.lpstrInitialDir = initialdir
        ofn.lpstrTitle = title
        ofn.lpstrDefExt = (
            defaultextension[1:]
            if defaultextension and defaultextension.startswith(".")
            else defaultextension
        )
        ofn.Flags = (
            OFN_EXPLORER | OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST | OFN_HIDEREADONLY
        )
        if multiple:
            ofn.Flags |= OFN_ALLOWMULTISELECT
        ok = comdlg32.GetOpenFileNameW(ctypes.byref(ofn))
        if not ok:
            return None
        s = file_buffer.value
        parts = [p for p in s.split("\x00") if p]
        if not parts:
            return None
        if multiple and len(parts) > 1:
            base = parts[0]
            return [os.path.join(base, name) for name in parts[1:]]
        return parts[0]

    def _win_save_file(
        title: str,
        initialdir: Optional[str],
        filetypes: Optional[FileTypes],
        defaultextension: Optional[str],
    ):
        buf_size = 4096
        file_buffer = ctypes.create_unicode_buffer(buf_size)
        ofn = OPENFILENAMEW()
        ofn.lStructSize = ctypes.sizeof(OPENFILENAMEW)
        ofn.lpstrFilter = _win_build_filter(filetypes)
        ofn.nFilterIndex = 1
        ofn.lpstrFile = ctypes.cast(file_buffer, wintypes.LPWSTR)
        ofn.nMaxFile = buf_size
        ofn.lpstrInitialDir = initialdir
        ofn.lpstrTitle = title
        ofn.lpstrDefExt = (
            defaultextension[1:]
            if defaultextension and defaultextension.startswith(".")
            else defaultextension
        )
        ofn.Flags = (
            OFN_EXPLORER | OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT | OFN_HIDEREADONLY
        )
        ok = comdlg32.GetSaveFileNameW(ctypes.byref(ofn))
        if not ok:
            return None
        return file_buffer.value or None

    import ctypes
    from ctypes import wintypes

    CLSID_FileOpenDialog = ctypes.GUID("{DC1C5A9C-E88A-4DDE-A5A1-60F82A20AEF7}")
    IID_IFileDialog = ctypes.GUID("{42f85136-db7e-439c-85f1-e4075d135fc8}")

    FOS_PICKFOLDERS = 0x00000020

    ole32 = ctypes.OleDLL("ole32")
    shell32 = ctypes.OleDLL("shell32")

    class IFileDialog(ctypes.c_void_p):
        pass

    def _win_select_folder(title: str, initialdir: str = None) -> str | None:
        ole32.CoInitialize(None)

        pfd = ctypes.POINTER(IFileDialog)()
        hr = ole32.CoCreateInstance(
            ctypes.byref(CLSID_FileOpenDialog),
            None,
            1,  # CLSCTX_INPROC_SERVER
            ctypes.byref(IID_IFileDialog),
            ctypes.byref(pfd),
        )
        if hr != 0:
            return None

        # 设置只选文件夹
        # vtbl[7] = SetOptions
        SetOptions = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_void_p, ctypes.c_uint)(
            ctypes.cast(pfd[0][7], ctypes.c_void_p)
        )
        SetOptions(pfd, FOS_PICKFOLDERS)

        # 设置标题
        if title:
            SetTitle = ctypes.CFUNCTYPE(
                ctypes.c_long, ctypes.c_void_p, wintypes.LPCWSTR
            )(ctypes.cast(pfd[0][17], ctypes.c_void_p))
            SetTitle(pfd, title)

        # Show
        Show = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_void_p, wintypes.HWND)(
            ctypes.cast(pfd[0][3], ctypes.c_void_p)
        )
        hr = Show(pfd, None)
        if hr != 0:
            return None

        # GetResult
        GetResult = ctypes.CFUNCTYPE(
            ctypes.c_long, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)
        )(ctypes.cast(pfd[0][20], ctypes.c_void_p))
        psi = ctypes.c_void_p()
        hr = GetResult(pfd, ctypes.byref(psi))
        if hr != 0:
            return None

        # GetDisplayName
        GetDisplayName = ctypes.WINFUNCTYPE(
            ctypes.c_long,
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.POINTER(wintypes.LPWSTR),
        )(ctypes.cast(psi[0][5], ctypes.c_void_p))
        ppsz = wintypes.LPWSTR()
        hr = GetDisplayName(psi, 0, ctypes.byref(ppsz))
        if hr != 0:
            return None

        folder = ppsz.value
        ole32.CoTaskMemFree(ppsz)
        ole32.CoUninitialize()
        return folder


# ------------------------------
# 非 Windows 平台：filedialpy
# ------------------------------
else:
    import filedialpy

    def _fd_open_file(
        title: str,
        initialdir: Optional[str],
        filetypes: Optional[FileTypes],
        defaultextension: Optional[str],
        multiple: bool,
    ):
        return filedialpy.open_file_dialog(
            title=title, directory=initialdir, filetypes=filetypes, multiple=multiple
        )

    def _fd_save_file(
        title: str,
        initialdir: Optional[str],
        filetypes: Optional[FileTypes],
        defaultextension: Optional[str],
    ):
        return filedialpy.saveFile(
            title=title,
            directory=initialdir,
            filetypes=filetypes,
            defaultextension=defaultextension,
        )

    def _fd_select_folder(title: str, initialdir: Optional[str]):
        return filedialpy.select_folder_dialog(title=title, directory=initialdir)


# ------------------------------
# 公共 API
# ------------------------------


def open_file(
    title: str = "Open File",
    initialdir: Optional[str] = None,
    filetypes: Optional[FileTypes] = None,
    defaultextension: Optional[str] = None,
    multiple: bool = False,
):
    if os.name == "nt":
        return _win_open_file(title, initialdir, filetypes, defaultextension, multiple)
    else:
        return _fd_open_file(title, initialdir, filetypes, defaultextension, multiple)


def save_file(
    title: str = "Save File",
    initialdir: Optional[str] = None,
    filetypes: Optional[FileTypes] = None,
    defaultextension: Optional[str] = None,
):
    if os.name == "nt":
        return _win_save_file(title, initialdir, filetypes, defaultextension)
    else:
        return _fd_save_file(title, initialdir, filetypes, defaultextension)


def select_folder(title: str = "Select Folder", initialdir: Optional[str] = None):
    if os.name == "nt":
        return _win_select_folder(title, initialdir)
    else:
        return _fd_select_folder(title, initialdir)


if __name__ == "__main__":
    print("[1] 选择文件……")
    print(open_file(title="选择文件", filetypes=[("All", "*.*")]))

    print("[2] 保存文件……")
    print(save_file(title="保存为", defaultextension=".txt"))

    print("[3] 选择文件夹……")
    print(select_folder(title="选择文件夹"))
