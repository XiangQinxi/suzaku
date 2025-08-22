import sys
import ctypes
import sdl2
import skia


def make_skia_surface(surface):
    """从 SDL_Surface 创建一个 Skia Surface"""
    width, height = surface.w, surface.h
    pixels_ptr = surface.pixels
    pitch = surface.pitch

    # 把 SDL 的像素数据包装成 Python buffer
    buf_type = ctypes.c_uint8 * (pitch * height)
    buf = buf_type.from_address(pixels_ptr)

    imageinfo = skia.ImageInfo.MakeN32Premul(width, height)
    return skia.Surface.MakeRasterDirect(imageinfo, buf, pitch)


def run():
    # 初始化 SDL
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print("SDL_Init Error:", sdl2.SDL_GetError())
        return

    # 创建窗口 (允许缩放)
    window = sdl2.SDL_CreateWindow(
        b"pySDL2 + skia-python (CPU Surface)",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        800,
        600,
        sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE,
    )
    if not window:
        print("SDL_CreateWindow Error:", sdl2.SDL_GetError())
        return

    # 获取初始窗口 surface
    surface = sdl2.SDL_GetWindowSurface(window).contents
    sk_surface = make_skia_surface(surface)

    running = True
    event = sdl2.SDL_Event()

    while running:
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                running = False
            if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                surface = sdl2.SDL_GetWindowSurface(window).contents
                sk_surface = make_skia_surface(surface)

                # ⚡ 立刻重绘一次，避免窗口空白
                with sk_surface as canvas:
                    canvas.clear(skia.ColorWHITE)
                    paint = skia.Paint(Color=skia.ColorBLUE)
                    canvas.drawRect(skia.Rect.MakeXYWH(100, 100, 200, 150), paint)
                sdl2.SDL_UpdateWindowSurface(window)
            elif event.window.event == sdl2.SDL_WINDOWEVENT_CLOSE:
                running = False

        # 用 Skia 绘制
        with sk_surface as canvas:
            canvas.clear(skia.ColorWHITE)

            paint = skia.Paint(Color=skia.ColorBLUE)
            canvas.drawRect(skia.Rect.MakeXYWH(100, 100, 200, 150), paint)

            paint = skia.Paint(Color=skia.ColorBLACK, AntiAlias=True)
            font = skia.Font(skia.Typeface("Arial"), 32)
            canvas.drawString("Hello Skia + SDL2 (CPU)", 100, 300, font, paint)

        # 更新窗口
        sdl2.SDL_UpdateWindowSurface(window)

    # 清理
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    sys.exit(0)


if __name__ == "__main__":
    run()
