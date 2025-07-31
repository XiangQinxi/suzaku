class Application:

    _instance = None

    def __init__(self):
        self.windows = []
        self.running = False
        self.visuals = {}
        self.init_glfw()
        if Application._instance is not None:
            raise RuntimeError("App is a singleton, use App.get_instance()")
        Application._instance = self

    # 这里用这个可以使`Window`的初始化更加简单，可以不选择填`parent=App`
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("App not initialized")
        return cls._instance

    def init_glfw(self):
        import glfw
        if not glfw.init():
            raise RuntimeError('glfw.init() failed')
        # 设置全局GLFW配置
        glfw.window_hint(glfw.STENCIL_BITS, 8)

    def get_visual_with_id(self, id):
        return self.visuals[id]

    def add(self, visual):
        self.visuals[visual.winfo_id()] = visual

    def add_window(self, window):
        """添加窗口到应用程序"""
        self.windows.append(window)
        # 将窗口的GLFW初始化委托给Application
        window.set_application(self)
        return self

    def run(self):
        import glfw
        if not self.windows:
            raise RuntimeError('至少需要添加一个窗口才能运行应用程序')

        self.running = True
        for window in self.windows:
            window.create_bind()

        # 主事件循环
        while self.running and not any(glfw.window_should_close(win.winfo_glfw_window()) for win in self.windows):
            glfw.poll_events()

            for window in self.windows:
                if window.visible():
                    with window.skia_surface(window.winfo_glfw_window()) as surface:
                        with surface as canvas:
                            if hasattr(window, 'draw_func') and window.draw_func:
                                window.draw_func(canvas)
                        surface.flushAndSubmit()
                    glfw.swap_buffers(window.winfo_glfw_window())

        # 清理资源
        self.cleanup()

    def cleanup(self):
        import glfw
        for window in self.windows:
            glfw.destroy_window(window.winfo_glfw_window())
        glfw.terminate()
        self.running = False

    def quit(self):
        """退出应用程序"""
        self.running = False