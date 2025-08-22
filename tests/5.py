import glfw
import skia
import ctypes
from ctypes import wintypes

# Win32 API
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


def blit_to_window(hwnd, width, height, data):
    hdc = user32.GetDC(hwnd)

    bmi = ctypes.create_string_buffer(40)
    ctypes.memset(bmi, 0, 40)
    ctypes.cast(bmi, ctypes.POINTER(ctypes.c_long))[0] = 40  # biSize
    ctypes.cast(bmi, ctypes.POINTER(ctypes.c_long))[1] = width  # biWidth
    ctypes.cast(bmi, ctypes.POINTER(ctypes.c_long))[
        2
    ] = -height  # biHeight (负值表示top-down)
    ctypes.cast(bmi, ctypes.POINTER(ctypes.c_short))[6] = 1  # biPlanes
    ctypes.cast(bmi, ctypes.POINTER(ctypes.c_short))[7] = 32  # biBitCount
    ctypes.cast(bmi, ctypes.POINTER(ctypes.c_long))[4] = 0  # biCompression (BI_RGB)

    gdi32.StretchDIBits(
        hdc,
        0,
        0,
        width,
        height,
        0,
        0,
        width,
        height,
        data,
        bmi,
        0,
        0x00CC0020,  # SRCCOPY
    )

    user32.ReleaseDC(hwnd, hdc)


def main():
    if not glfw.init():
        raise RuntimeError("Failed to init GLFW")

    glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)  # 禁用OpenGL
    window = glfw.create_window(640, 480, "GLFW + Skia CPU (No OpenGL)", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create window")

    hwnd = glfw.get_win32_window(window)  # 需要 pyGLFW 提供 get_win32_window 扩展

    width, height = glfw.get_framebuffer_size(window)
    info = skia.ImageInfo.MakeN32Premul(width, height)
    surface = skia.Surface.MakeRaster(info)
    canvas = surface.getCanvas()

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Skia CPU 渲染
        canvas.clear(skia.ColorWHITE)
        paint = skia.Paint(Color=skia.ColorBLUE)
        canvas.drawRect(skia.Rect.MakeXYWH(100, 100, 200, 150), paint)
        paint.setColor(skia.ColorRED)
        paint.setAntiAlias(True)
        canvas.drawCircle(300, 300, 80, paint)

        # 导出像素
        image = surface.makeImageSnapshot()
        pixels = image.tobytes()

        # CPU blit 到窗口
        blit_to_window(hwnd, width, height, pixels)

    glfw.terminate()


if __name__ == "__main__":
    main()
