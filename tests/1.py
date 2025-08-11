import glfw
import OpenGL.GL as gl
from ctypes import windll, wintypes, byref
import ctypes


def create_custom_titlebar_window():
    # 初始化GLFW
    if not glfw.init():
        return None

    # 设置窗口提示 - 隐藏装饰
    glfw.window_hint(glfw.DECORATED, glfw.FALSE)
    glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)

    # 创建窗口
    window = glfw.create_window(800, 600, "Custom Titlebar", None, None)
    if not window:
        glfw.terminate()
        return None

    glfw.make_context_current(window)

    # 获取Windows句柄
    hwnd = glfw.get_win32_window(window)

    # 设置窗口样式以支持拖拽
    style = windll.user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
    style |= 0x00800000  # WS_BORDER
    windll.user32.SetWindowLongW(hwnd, -16, style)

    return window, hwnd


def handle_titlebar_drag(window, hwnd, mouse_x, mouse_y, titlebar_height=30):
    """处理标题栏拖拽"""
    if mouse_y < titlebar_height:  # 鼠标在标题栏区域
        # 发送拖拽消息
        windll.user32.ReleaseCapture()
        windll.user32.SendMessageW(hwnd, 0x00A1, 2, 0)  # WM_NCLBUTTONDOWN, HTCAPTION


window, hwnd = create_custom_titlebar_window()
