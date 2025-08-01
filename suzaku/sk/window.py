from ..base.window import Window
import skia


class SkWindow(Window):
    def __init__(self, *args, themename="light", **kwargs):
        """
        初始化

        :param args: Window参数
        :param themename: 主题名称
        :param kwargs: Window参数
        """
        super().__init__(*args, **kwargs)

        from ..themes import theme

        self.theme = theme
        self.theme.use_theme(themename)

        self.window_attr["name"] = "sk_window"
        self.window_attr["layout"] = None
        self.draws = []
        self.visuals = []
        self.previous_visual = None  # 跟踪上一个鼠标悬停的元素

        self.set_draw_func(self.draw)
        self.bind("mouse_motion", self._motion, add=True)
        self.bind("mouse_pressed", self._mouse)
        self.bind("mouse_released", self._mouse_released)

        #self.bind("window_mouse_enter", self._motion, add=True)
        #self.bind("window_mouse_leave", self._motion, add=True)

    def _mouse(self):
        """
        回调组件接收鼠标按下自己事件
        :return: None
        """
        from ..base.event import Event
        event = Event(
            x=self.window_attr["mouse_x"],
            y=self.window_attr["mouse_y"],
            rootx=self.window_attr["mouse_rootx"],
            rooty=self.window_attr["mouse_rooty"]
        )
        for visual in self.visuals:
            if (visual.winfo_x() <= event.x <= visual.winfo_x() + visual.winfo_width() and
                    visual.winfo_y() <= event.y <= visual.winfo_y() + visual.winfo_height()):
                visual.event_generate("mouse_pressed", event)
                break

    from ..base.event import Event

    def _motion(self, evt: Event):
        """
        回调组件接收鼠标移动、进入、离开事件
        :param evt: 事件对象
        :return: None
        """
        self.window_attr["mouse_x"] = evt.x
        self.window_attr["mouse_y"] = evt.y
        self.window_attr["mouse_rootx"] = evt.x + self.winfo_x()
        self.window_attr["mouse_rooty"] = evt.y + self.winfo_y()
        current_visual = None
        from ..base.event import Event
        event = Event(x=evt.x, y=evt.y, rootx=self.window_attr["mouse_rootx"], rooty=self.window_attr["mouse_rooty"])

        # 找到当前鼠标所在的视觉元素
        for visual in reversed(self.visuals):
            if (visual.winfo_x() <= evt.x <= visual.winfo_x() + visual.winfo_width() and
                visual.winfo_y() <= evt.y <= visual.winfo_y() + visual.winfo_height()):
                current_visual = visual
                break

        # 处理上一个元素的离开事件
        if self.previous_visual and self.previous_visual != current_visual:
            self.cursor(self.default_cursor())
            self.previous_visual.event_generate("mouse_leave", event)
            self.previous_visual.is_mouse_enter = False

        # 处理当前元素的进入和移动事件
        if current_visual:
            if current_visual.winfo_visible():
                if not current_visual.is_mouse_enter:
                    self.cursor(current_visual.visual_attr["cursor"])
                    current_visual.event_generate("mouse_enter", event)
                    current_visual.is_mouse_enter = True
                else:
                    self.cursor(current_visual.visual_attr["cursor"])
                    current_visual.event_generate("mouse_motion", event)
                self.previous_visual = current_visual
        else:
            self.previous_visual = None

    def set_layout(self, layout) -> None:
        """
        设置窗口布局

        :param layout: 布局类 Boxes、Puts等
        :return: None
        """
        self.window_attr["layout"] = layout

    def add_draw(self, draw_func) -> None:
        """
        添加可视化元素绘制函数

        :param draw_func: 绘制函数
        :return: None
        """
        self.draws.append(draw_func)

    def remove_draw(self, draw_func) -> None:
        """
        移除可视化元素绘制函数

        :param draw_func: 绘制函数
        :return: None
        """
        self.draws.remove(draw_func)

    def draw(self, canvas: skia.Surfaces) -> None:
        """
        绘制Skia画布与其上的可视化元素

        :param canvas: Skia画布
        :return: None
        """
        from ..style.color import color
        canvas.clear(color(self.theme.get_theme()["SkWindow"]["bg"]))

        for i, f in enumerate(self.draws):
            #print(i, f)
            if self.visuals[i].winfo_visible():
                f(canvas)
        return None

    def winfo_layout(self) -> type:
        """
        获取窗口的布局

        :return: 布局类
        """
        return self.window_attr["layout"]

    def _mouse_released(self) -> None:
        """
        鼠标释放事件处理函数，将会触发mouse_release事件。

        :return: None
        """
        from ..base.event import Event
        event = Event(
            x=self.window_attr["mouse_x"],
            y=self.window_attr["mouse_y"],
            rootx=self.window_attr["mouse_rootx"],
            rooty=self.window_attr["mouse_rooty"]
        )
        for visual in self.visuals:
            if visual.is_mouse_pressed:
                visual.event_generate("mouse_released", event)
                visual.is_mouse_pressed = False
        return None
