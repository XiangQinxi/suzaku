import glfw
import OpenGL.GL as gl


def main():
    # 初始化GLFW
    if not glfw.init():
        return

    # 设置窗口提示：启用DPI缩放感知 (GLFW 3.3+)
    glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, glfw.TRUE)  # macOS
    glfw.window_hint(glfw.SCALE_TO_MONITOR, glfw.TRUE)  # Windows/Linux

    # 创建窗口
    window = glfw.create_window(800, 600, "DPI-Aware Window", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # 获取初始DPI缩放因子
    x_scale, y_scale = glfw.get_window_content_scale(window)
    print(f"Initial content scale: {x_scale:.1f}x{y_scale:.1f}")

    # 设置DPI变化回调
    def content_scale_callback(win, x_scale, y_scale):
        print(f"Content scale changed: {x_scale:.1f}x{y_scale:.1f}")
        # 在此处更新UI元素尺寸/重新加载纹理等
        gl.glViewport(0, 0, int(800 * x_scale), int(600 * y_scale))

    glfw.set_window_content_scale_callback(window, content_scale_callback)

    # 主循环
    while not glfw.window_should_close(window):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
