import contextlib, glfw, skia, sys
from OpenGL import GL

WIDTH, HEIGHT = 640, 480

# 全局变量存储绘图函数
draw_func = None

def on_framebuffer_size_changed(window, width, height):
    # 当窗口大小变化时重新创建表面并重绘
    with skia_surface(window) as surface:
        with surface as canvas:
            if draw_func:
                draw_func(canvas)
        surface.flushAndSubmit()
        glfw.swap_buffers(window)

@contextlib.contextmanager
def glfw_window():
    if not glfw.init():
        raise RuntimeError('glfw.init() failed')
    glfw.window_hint(glfw.STENCIL_BITS, 8)
    # see https://www.glfw.org/faq#macos
    if sys.platform.startswith("darwin"):
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(WIDTH, HEIGHT, '', None, None)
    glfw.make_context_current(window)
    # 设置帧缓冲大小变化的回调函数
    glfw.set_framebuffer_size_callback(window, on_framebuffer_size_changed)
    yield window
    glfw.terminate()

@contextlib.contextmanager
def skia_surface(window):
    context = skia.GrDirectContext.MakeGL()
    (fb_width, fb_height) = glfw.get_framebuffer_size(window)
    backend_render_target = skia.GrBackendRenderTarget(
        fb_width,
        fb_height,
        0,  # sampleCnt
        0,  # stencilBits
        skia.GrGLFramebufferInfo(0, GL.GL_RGBA8))
    surface = skia.Surface.MakeFromBackendRenderTarget(
        context, backend_render_target, skia.kBottomLeft_GrSurfaceOrigin,
        skia.kRGBA_8888_ColorType, skia.ColorSpace.MakeSRGB())
    assert surface is not None
    yield surface
    context.releaseResourcesAndAbandonContext()

def draw(canvas):
    # 这里定义你的绘图逻辑
    canvas.clear(skia.ColorWHITE)
    canvas.drawCircle(100, 100, 40, skia.Paint(Color=skia.ColorGREEN))

# 设置全局绘图函数
draw_func = draw

with glfw_window() as window:
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    with skia_surface(window) as surface:
        with surface as canvas:
            draw(canvas)
        surface.flushAndSubmit()
        glfw.swap_buffers(window)

        while (glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS
            and not glfw.window_should_close(window)):
            glfw.wait_events()
