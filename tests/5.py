import glfw


class Window:
    def __init__(self, width=800, height=600, title="Demo"):
        if not glfw.init():
            raise RuntimeError("GLFW init failed")

        self._win = glfw.create_window(width, height, title, None, None)
        if not self._win:
            glfw.terminate()
            raise RuntimeError("GLFW window creation failed")

    def geometry(self, spec: str | None = None) -> str | None:
        """
        Tkinter 风格 geometry 方法:
          - 设置: "WIDTHxHEIGHT+X+Y" / "WIDTHxHEIGHT" / "+X+Y"
          - 获取: 返回 "WIDTHxHEIGHT+X+Y"
        """
        if spec is None:
            # --- 获取 ---
            width, height = glfw.get_window_size(self._win)
            x, y = glfw.get_window_pos(self._win)
            return f"{width}x{height}+{x}+{y}"

        # --- 设置 ---
        width, height = None, None
        x, y = None, None

        # 判断是否包含大小
        if "x" in spec:
            wh, _, rest = spec.partition("+")
            width, height = map(int, wh.split("x"))
            if rest:
                x, y = map(int, rest.split("+"))
        elif spec.startswith("+"):
            x, y = map(int, spec[1:].split("+"))

        # 设置窗口大小
        if width and height:
            glfw.set_window_size(self._win, width, height)
        # 设置窗口位置
        if x is not None and y is not None:
            glfw.set_window_pos(self._win, x, y)

    def mainloop(self):
        while not glfw.window_should_close(self._win):
            glfw.poll_events()
        glfw.terminate()


if __name__ == "__main__":
    win = Window()
    # win.geometry("300x300")  # 只设置大小
    win.geometry("+200+150")  # 只设置位置
    # win.geometry("640x480+100+50")  # 大小+位置
    print("当前几何信息:", win.geometry())  # 获取
    win.mainloop()
