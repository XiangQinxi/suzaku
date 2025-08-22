import sys
import sdl2
import sdl2.video
import OpenGL.GL as gl
import skia


def run():
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print("SDL_Init Error:", sdl2.SDL_GetError())
        return

    # OpenGL 属性
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(
        sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE
    )

    # 创建窗口 (OpenGL 渲染)
    window = sdl2.SDL_CreateWindow(
        b"pySDL2 + Skia GPU Surface",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        800,
        600,
        sdl2.SDL_WINDOW_OPENGL
        | sdl2.SDL_WINDOW_RESIZABLE
        | sdl2.SDL_WINDOW_ALLOW_HIGHDPI,
    )
    if not window:
        print("SDL_CreateWindow Error:", sdl2.SDL_GetError())
        return

    # 创建 OpenGL 上下文
    gl_context = sdl2.SDL_GL_CreateContext(window)
    sdl2.SDL_GL_MakeCurrent(window, gl_context)

    # 初始化 Skia GPU 绑定
    context = skia.GrDirectContext.MakeGL()

    # 获取窗口大小
    w, h = ctypes.c_int(), ctypes.c_int()
    sdl2.SDL_GL_GetDrawableSize(window, w, h)
    width, height = w.value, h.value

    # 创建 Skia GPU 渲染目标
    def make_surface(width, height):
        fb_id = gl.glGetIntegerv(gl.GL_FRAMEBUFFER_BINDING)
        backend_rt = skia.GrBackendRenderTarget(
            width,
            height,
            0,  # sampleCnt
            0,  # stencilBits
            skia.GrGLFramebufferInfo(fb_id, gl.GL_RGBA8),
        )
        return skia.Surface.MakeFromBackendRenderTarget(
            context,
            backend_rt,
            skia.kBottomLeft_GrSurfaceOrigin,
            skia.kRGBA_8888_ColorType,
            skia.ColorSpace.MakeSRGB(),
        )

    sk_surface = make_surface(width, height)

    running = True
    event = sdl2.SDL_Event()

    while running:
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                running = False
            elif event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_SIZE_CHANGED:
                    sdl2.SDL_GL_GetDrawableSize(window, w, h)
                    width, height = w.value, h.value
                    sk_surface = make_surface(width, height)

                elif event.window.event == sdl2.SDL_WINDOWEVENT_CLOSE:
                    running = False

        if not running:
            break

        # --- Skia 绘制 ---
        with sk_surface as canvas:
            canvas.clear(skia.ColorWHITE)

            paint = skia.Paint(Color=skia.ColorRED)
            canvas.drawCircle(width // 2, height // 2, 100, paint)

        context.flush()
        sdl2.SDL_GL_SwapWindow(window)

    # --- 清理 ---
    sdl2.SDL_GL_DeleteContext(gl_context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    sys.exit(0)  # <== 确保 Python 进程退出


if __name__ == "__main__":
    import ctypes

    run()
