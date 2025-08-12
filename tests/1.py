import sys
import os
import time
from PIL import Image
import win32gui, win32con


def capture_window_region(window_title=None, window_handle=None,
                          save_path="screenshot.png"):
    """
    截取指定窗口的画面（即使被遮挡）

    参数:
        window_title: 窗口标题（部分匹配）
        window_handle: 窗口句柄（优先使用）
        save_path: 截图保存路径

    返回:
        PIL.Image 对象
    """
    platform = sys.platform.lower()

    if platform.startswith('win'):
        return _capture_win(window_title, window_handle, save_path)
    elif platform.startswith('darwin'):
        return _capture_mac(window_title, window_handle, save_path)
    elif platform.startswith('linux'):
        return _capture_linux(window_title, window_handle, save_path)
    else:
        raise OSError("Unsupported operating system")


# ===== Windows 实现 =====
def _capture_win(window_title, window_handle, save_path):
    try:
        import win32gui
        import win32ui
        import win32con
        import win32api
    except ImportError:
        raise ImportError("pywin32 required. Install with: pip install pywin32")

    # 获取窗口句柄
    if window_handle:
        hwnd = window_handle
    elif window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if not hwnd:
            # 尝试模糊匹配
            def callback(hwnd, titles):
                if win32gui.IsWindowVisible(
                        hwnd) and window_title.lower() in win32gui.GetWindowText(
                        hwnd).lower():
                    titles.append(hwnd)

            titles = []
            win32gui.EnumWindows(callback, titles)
            if titles:
                hwnd = titles[0]
            else:
                raise ValueError(f"Window '{window_title}' not found")
    else:
        # 获取前台窗口
        hwnd = win32gui.GetForegroundWindow()

    # 获取窗口位置和大小
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    # 创建设备上下文
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

    # 选择位图对象
    saveDC.SelectObject(saveBitMap)

    # 截取窗口内容（即使被遮挡）
    result = saveDC.BitBlt(
        (0, 0),
        (width, height),
        mfcDC,
        (0, 0),
        win32con.SRCCOPY | win32con.CAPTUREBLT
    )

    if result is None:
        raise RuntimeError("Failed to capture window")

    # 获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    # 创建PIL图像
    image = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1
    )

    # 清理资源
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    # 保存图像
    if save_path:
        image.save(save_path)
        print(f"Screenshot saved to {save_path}")

    return image


# ===== macOS 实现 =====
def _capture_mac(window_title, window_handle, save_path):
    try:
        from AppKit import NSApplication, NSWindow, NSRect, NSImage, NSBitmapImageRep
        import Quartz
    except ImportError:
        raise ImportError("PyObjC required. Install with: pip install pyobjc")

    # 获取窗口ID
    if window_handle:
        window_id = window_handle
    else:
        # 查找窗口
        app = NSApplication.sharedApplication()
        windows = app.windows()

        target_window = None
        for window in windows:
            if window_title and window_title.lower() in window.title().lower():
                target_window = window
                break
            elif not window_title and window.isMainWindow():
                target_window = window
                break

        if not target_window:
            raise ValueError(f"Window '{window_title}' not found")

        window_id = window.windowNumber()

    # 创建屏幕截图
    cg_image = Quartz.CGWindowListCreateImage(
        Quartz.CGRectNull,
        Quartz.kCGWindowListOptionIncludingWindow,
        window_id,
        Quartz.kCGWindowImageBoundsIgnoreFraming |
        Quartz.kCGWindowImageShouldBeOpaque
    )

    if not cg_image:
        raise RuntimeError("Failed to capture window")

    # 转换为NSImage
    size = Quartz.CGImageGetWidth(cg_image), Quartz.CGImageGetHeight(cg_image)
    image_rep = NSBitmapImageRep.alloc().initWithCGImage_(cg_image)
    ns_image = NSImage.alloc().initWithSize_(size)
    ns_image.addRepresentation_(image_rep)

    # 转换为PIL图像
    tiff_data = ns_image.TIFFRepresentation()
    image = Image.open(io.BytesIO(tiff_data))

    # 保存图像
    if save_path:
        image.save(save_path)
        print(f"Screenshot saved to {save_path}")

    return image


# ===== Linux 实现 (X11) =====
def _capture_linux(window_title, window_handle, save_path):
    try:
        from Xlib import display, X
        from Xlib.ext import xfixes
    except ImportError:
        raise ImportError("python-xlib required. Install with: pip install python-xlib")

    # 获取显示连接
    d = display.Display()
    root = d.screen().root

    # 获取窗口ID
    if window_handle:
        window_id = window_handle
    else:
        # 查找窗口
        window_id = None
        windows = root.query_tree().children

        for win in windows:
            name = win.get_wm_name()
            if name and window_title and window_title.lower() in name.lower():
                window_id = win.id
                break

        if not window_id:
            # 尝试活动窗口
            net_active_window = d.intern_atom('_NET_ACTIVE_WINDOW')
            active_window = root.get_full_property(net_active_window, X.AnyPropertyType)
            if active_window:
                window_id = active_window.value[0]
            else:
                raise ValueError(f"Window '{window_title}' not found")

    # 获取窗口几何信息
    window = d.create_resource_object('window', window_id)
    geometry = window.get_geometry()

    # 使用XFixes扩展获取窗口内容（即使被遮挡）
    xfixes = d.xfixes_query_version()
    region = xfixes.FetchRegion(d, window_id)

    # 创建图像
    image = root.get_image(
        geometry.x,
        geometry.y,
        geometry.width,
        geometry.height,
        X.ZPixmap,
        0xffffffff
    )

    # 转换为PIL图像
    pil_image = Image.frombytes(
        "RGB",
        (geometry.width, geometry.height),
        image.data,
        "raw",
        "BGRX",
        0,
        1
    )

    # 保存图像
    if save_path:
        pil_image.save(save_path)
        print(f"Screenshot saved to {save_path}")

    return pil_image


# ===== 使用示例 =====
if __name__ == "__main__":
    # 示例1: 截取当前活动窗口
    print("Capturing active window...")
    capture_window_region(save_path="active_window.png")

    # 示例2: 截取指定标题的窗口
    print("Capturing Notepad window...")
    try:
        capture_window_region(window_title="Notepad", save_path="notepad.png")
    except Exception as e:
        print(f"Error: {e}")

    # 示例3: 截取特定进程ID的窗口
    if sys.platform == 'win32':
        import win32process
        import win32gui


        # 查找Chrome窗口
        def find_chrome_window():
            def callback(hwnd, hwnds):
                if win32gui.IsWindowVisible(hwnd):
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    try:
                        exe_name = win32process.GetModuleFileNameEx(
                            win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION,
                                                 False, pid),
                            0
                        )
                        if "chrome.exe" in exe_name.lower():
                            hwnds.append(hwnd)
                    except:
                        pass
                return True

            hwnds = []
            win32gui.EnumWindows(callback, hwnds)
            return hwnds[0] if hwnds else None


        chrome_hwnd = find_chrome_window()
        if chrome_hwnd:
            print("Capturing Chrome window...")
            capture_window_region(window_handle=chrome_hwnd, save_path="chrome.png")
