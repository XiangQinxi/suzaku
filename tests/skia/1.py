import sys
import ctypes
import sdl2
import skia


def run():
    # 初始化 SDL
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print("SDL_Init Error:", sdl2.SDL_GetError())
        return

    # 创建 SDL 窗口
    window = sdl2.SDL_CreateWindow(
        b"pySDL2 + skia-python demo",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        800,
        600,
        sdl2.SDL_WINDOW_SHOWN
        | sdl2.SDL_WINDOW_ALLOW_HIGHDPI
        | sdl2.SDL_WINDOW_RESIZABLE,
    )

    if not window:
        print("SDL_CreateWindow Error:", sdl2.SDL_GetError())
        sdl2.SDL_Quit()
        return

    # 获取窗口 surface
    surface = sdl2.SDL_GetWindowSurface(window).contents

    # SDL surface 参数
    width, height = surface.w, surface.h
    pixels_ptr = surface.pixels
    pitch = surface.pitch

    # 把 SDL pixels 包装成 ctypes buffer
    buf_type = ctypes.c_uint8 * (pitch * height)
    buf = buf_type.from_address(pixels_ptr)

    # 创建 Skia surface
    imageinfo = skia.ImageInfo.MakeN32Premul(width, height)
    sk_surface = skia.Surface.MakeRasterDirect(imageinfo, buf, pitch)

    running = True
    event = sdl2.SDL_Event()

    while running:
        # 处理事件
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                running = False

        # Skia 绘制
        with sk_surface as canvas:
            canvas.clear(skia.ColorWHITE)

            paint = skia.Paint(Color=skia.ColorBLUE)
            canvas.drawRect(skia.Rect.MakeXYWH(100, 100, 200, 150), paint)

            paint = skia.Paint(Color=skia.ColorBLACK, AntiAlias=True)
            font = skia.Font(skia.Typeface("Arial"), 32)
            canvas.drawString("Hello Skia + SDL2", 100, 300, font, paint)

        # 更新 SDL 窗口
        sdl2.SDL_UpdateWindowSurface(window)

    # 清理
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()


if __name__ == "__main__":
    run()
