# TK Experiments - Frameless Window
# The experiments creates a frameless window with basic functions in tkinter

import tkinter as tk
import tttk

"""
Due to the inactivity of project tttk on PyPI, a normal installation of tttk with pip will not be 
able to make this file work. If necessary, please use latest tttk release from GitHub, or use 
latest release of github.com/totowang-hhh/TK-Experiments for an original usable version of the 
frameless window experiment with built-in tttk module.

                                                                        —— 2025/10/05 rgzz666
"""

class FramelessTk(tk.Tk):
    def __init__(self, dragheight=28, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.dragheight = dragheight
        self.resize_dragwidth = 15
        # Things for internal use
        self._alive = True
        self._pointerdown_x = 0
        self._pointerdown_y = 0
        self._original_w = 0
        self._original_h = 0
        self._dragging = False
        self._last_normal_w = 0
        self._last_notmal_h = 0
        self._last_notmal_x = 0
        self._last_notmal_y = 0
        self._is_zoomed = False
        # Action Buttons
        self.action_btns = tk.Frame(self, height=16)
        self.minimize_btn = tttk.FlatButton(
            self.action_btns,
            text="0",
            font=("webdings", 10),
            bg="#ffffff",
            fg="#000000",
            floatingbg="#cccccc",
            command=self.iconify,
        )
        self.maximize_btn = tttk.FlatButton(
            self.action_btns,
            text="1",
            font=("webdings", 10),
            bg="#ffffff",
            fg="#000000",
            floatingbg="#cccccc",
            command=self.toggle_normal_zoomed,
        )
        self.close_btn = tttk.FlatButton(
            self.action_btns,
            text="r",
            font=("webdings", 10),
            bg="#ffffff",
            fg="#000000",
            floatingbg="#ff0000",
            floatingfg="#ffffff",
            command=lambda: self.destroy(from_close_button=True),
        )
        self.minimize_btn.pack(side=tk.LEFT, fill=tk.Y)
        self.maximize_btn.pack(side=tk.LEFT, fill=tk.Y)
        self.close_btn.pack(side=tk.LEFT, fill=tk.Y)
        # self.action_btns.place(x=0,y=0)
        # Where the magic works
        self.tbicon_win = (
            tk.Toplevel()
        )  # In my plan, this window is aimed to show the taskbar icon, and it should be covered with the frameless window to be invisible.
        self.tbicon_win.title("TK FramelessWindow")
        # self.tbicon_win.geometry("10x72+"+str(self.winfo_x()+2)+"+"+str(self.winfo_y()+2))
        tk.Label(self.tbicon_win, text="TK FramelessWindow").pack()
        tk.Label(self.tbicon_win, text="by rgzz666").pack()
        self.tbicon_win.bind("<FocusIn>", lambda event: tk.Tk.deiconify(self))
        # Initialization
        self.geometry("540x360+50+50")
        self.bind("<B1-Motion>", lambda event: self._on_mouse_drag(event))
        self.bind("<Button-1>", lambda event: self._on_button_down(event))
        self.bind("<ButtonRelease-1>", lambda event: self._on_button_release(event))
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.tbicon_win.protocol("WM_DELETE_WINDOW", self.destroy)

    def update(self):
        if not self._alive:
            return
        tk.Tk.update(self)
        if not self._alive:
            return
        self.tbicon_win.update()
        self.tbicon_win.geometry(
            "160x80+" + str(self.winfo_x() + 2) + "+" + str(self.winfo_y() + 2)
        )
        self.action_btns.place(
            x=self.winfo_width() - self.action_btns.winfo_width(), y=0
        )
        self.action_btns.lift()

    def mainloop(self):
        while self._alive:
            self.update()

    def destroy(self, from_close_button=False):
        self.unbind("<B1-Motion>")
        self.unbind("<Button-1>")
        self.unbind("<ButtonRelease-1>")
        self._alive = False
        self.tbicon_win.destroy()
        if not from_close_button:  # If not triggered by the close button
            tk.Tk.destroy(self)
        else:  # If triggered by the close button
            self.withdraw()  # Only use withdraw() and let _on_button_down() to do the rest
        # tk.Tk.destroy(self)

    def int_geometry(self, w, h, x=None, y=None):
        if x == None or y == None:
            self.geometry("{w}x{h}".format(w=str(w), h=str(h)))
        else:
            self.geometry(
                "{w}x{h}+{x}+{y}".format(w=str(w), h=str(h), x=str(x), y=str(y))
            )

    def iconify(self):
        self.tbicon_win.iconify()
        self.withdraw()

    def deiconify(self):
        self.tbicon_win.deiconify()
        tk.Tk.deiconify(self)

    def _on_button_down(self, event):
        if (
            not self._alive
        ):  # The Button-1 will still be triggered when pressing X button
            tk.Tk.destroy(
                self
            )  # Then this line destroys the window finally instead of the destroy() function of the base class
            return  # And finally quits the function to prevent further errors
        self._pointerdown_x = event.x
        self._pointerdown_y = event.y
        self._original_w = self.winfo_width()
        self._original_h = self.winfo_height()

    def _on_mouse_drag(self, event):
        self._dragging = True
        if not self._alive:
            return
        if (
            event.x >= self.winfo_width() - self.resize_dragwidth
            or event.y >= self.winfo_height() - self.resize_dragwidth
        ):  # If user tries to resize bot not to move the window
            self._resize(event)
        else:  # Otherwise the user must trying to drag and move the window
            self._move(event)

    def _move(self, event, coords: list = [0, 0], ignore_drag_pos_check=False):
        if event.y <= self.dragheight or ignore_drag_pos_check:
            if event.type.__str__() == "4":
                coords[0], coords[1] = event.x, event.y
            else:
                x, y = event.x - coords[0], event.y - coords[1]
                lx, ly = map(int, self.geometry().split("+")[-2:])
                self.geometry(
                    "%dx%d+%d+%d"
                    % (
                        self.winfo_width(),
                        self.winfo_height(),
                        lx + x - self._pointerdown_x,
                        ly + y - self._pointerdown_y,
                    )
                )
        else:
            if type(self.dragheight) == str:
                if self.dragheight.lower() == "full":
                    self.move(event, ignore_drag_pos_check=True)

    def _resize(self, event):
        if (
            event.x >= self.winfo_width() - self.resize_dragwidth
            and event.y >= self.winfo_height() - self.resize_dragwidth
        ):  # If dragging the right-bottom corner of the window
            self.config(cursor="sizing")
            self.int_geometry(
                event.x + self._original_w - self._pointerdown_x,
                event.y + self._original_h - self._pointerdown_y,
            )  # Then allow freely resizing the window
        elif event.x >= self.winfo_width() - self.resize_dragwidth and (
            not event.y >= self.winfo_height() - self.resize_dragwidth
        ):  # If dragging the right edge of the window
            self.config(cursor="sb_h_double_arrow")
            self.int_geometry(
                event.x + self._original_w - self._pointerdown_x, self._original_h
            )  # Then allow horizentally resizing the window
        elif (
            not event.x >= self.winfo_width() - self.resize_dragwidth
        ) and event.y >= self.winfo_height() - self.resize_dragwidth:  # If dragging the bottom edge of the window
            self.config(cursor="sb_v_double_arrow")
            self.int_geometry(
                self._original_w, event.y + self._original_h - self._pointerdown_y
            )  # Then allow veritically resizing the window

    def _on_button_release(self, event):
        self._dragging = False
        self.config(cursor="arrow")

    def make_zoomed(self):
        self._last_normal_w = self.winfo_width()
        self._last_normal_h = self.winfo_height()
        self._last_normal_x = self.winfo_x()
        self._last_normal_y = self.winfo_y()
        self.tbicon_win.state("zoomed")
        self.tbicon_win.update()
        self.int_geometry(
            self.tbicon_win.winfo_width(),
            self.tbicon_win.winfo_height() + 24,
            self.tbicon_win.winfo_x() + 8,
            self.tbicon_win.winfo_y() + 8,
        )
        self.tbicon_win.state("normal")
        self.tbicon_win.update()
        self.lift()
        self.maximize_btn["text"] = "2"
        self._is_zoomed = True

    def make_normal(self):
        self.int_geometry(
            self._last_normal_w,
            self._last_normal_h,
            self._last_normal_x,
            self._last_normal_y,
        )
        self.maximize_btn["text"] = "1"
        self._is_zoomed = False

    def toggle_normal_zoomed(self):
        if self._is_zoomed:
            self.make_normal()
        else:
            self.make_zoomed()


class FramelessToplevel(tk.Toplevel):
    def __init__(self, dragheight=28, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.dragheight = dragheight
        self.resize_dragwidth = 15
        # Things for internal use
        self._alive = True
        self._pointerdown_x = 0
        self._pointerdown_y = 0
        self._original_w = 0
        self._original_h = 0
        self._dragging = False
        self._last_normal_w = 0
        self._last_notmal_h = 0
        self._last_notmal_x = 0
        self._last_notmal_y = 0
        self._is_zoomed = False
        # Action Buttons
        self.action_btns = tk.Frame(self, height=16)
        self.minimize_btn = tttk.FlatButton(
            self.action_btns,
            text="0",
            font=("webdings", 10),
            bg="#ffffff",
            fg="#000000",
            floatingbg="#cccccc",
            command=self.iconify,
        )
        self.maximize_btn = tttk.FlatButton(
            self.action_btns,
            text="1",
            font=("webdings", 10),
            bg="#ffffff",
            fg="#000000",
            floatingbg="#cccccc",
            command=self.toggle_normal_zoomed,
        )
        self.close_btn = tttk.FlatButton(
            self.action_btns,
            text="r",
            font=("webdings", 10),
            bg="#ffffff",
            fg="#000000",
            floatingbg="#ff0000",
            floatingfg="#ffffff",
            command=lambda: self.destroy(from_close_button=True),
        )
        self.minimize_btn.pack(side=tk.LEFT, fill=tk.Y)
        self.maximize_btn.pack(side=tk.LEFT, fill=tk.Y)
        self.close_btn.pack(side=tk.LEFT, fill=tk.Y)
        # self.action_btns.place(x=0,y=0)
        # Where the magic works
        self.tbicon_win = (
            tk.Toplevel()
        )  # In my plan, this window is aimed to show the taskbar icon, and it should be covered with the frameless window to be invisible.
        self.tbicon_win.title("TK FramelessWindow")
        # self.tbicon_win.geometry("10x72+"+str(self.winfo_x()+2)+"+"+str(self.winfo_y()+2))
        tk.Label(self.tbicon_win, text="TK FramelessWindow").pack()
        tk.Label(self.tbicon_win, text="by rgzz666").pack()
        self.tbicon_win.bind("<FocusIn>", lambda event: tk.Toplevel.deiconify(self))
        # Initialization
        self.geometry("540x360+50+50")
        self.bind("<B1-Motion>", lambda event: self._on_mouse_drag(event))
        self.bind("<Button-1>", lambda event: self._on_button_down(event))
        self.bind("<ButtonRelease-1>", lambda event: self._on_button_release(event))
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.tbicon_win.protocol("WM_DELETE_WINDOW", self.destroy)

    def update(self):
        if not self._alive:
            return
        tk.Toplevel.update(self)
        if not self._alive:
            return
        self.tbicon_win.update()
        self.tbicon_win.geometry(
            "160x80+" + str(self.winfo_x() + 2) + "+" + str(self.winfo_y() + 2)
        )
        self.action_btns.place(
            x=self.winfo_width() - self.action_btns.winfo_width(), y=0
        )
        self.action_btns.lift()

    def mainloop(self):
        while self._alive:
            self.update()

    def destroy(self, from_close_button=False):
        self.unbind("<B1-Motion>")
        self.unbind("<Button-1>")
        self.unbind("<ButtonRelease-1>")
        self._alive = False
        self.tbicon_win.destroy()
        if not from_close_button:  # If not triggered by the close button
            tk.Toplevel.destroy(self)
        else:  # If triggered by the close button
            self.withdraw()  # Only use withdraw() and let _on_button_down() to do the rest
        # tk.Toplevel.destroy(self)

    def int_geometry(self, w, h, x=None, y=None):
        if x == None or y == None:
            self.geometry("{w}x{h}".format(w=str(w), h=str(h)))
        else:
            self.geometry(
                "{w}x{h}+{x}+{y}".format(w=str(w), h=str(h), x=str(x), y=str(y))
            )

    def iconify(self):
        self.tbicon_win.iconify()
        self.withdraw()

    def deiconify(self):
        self.tbicon_win.deiconify()
        tk.Toplevel.deiconify(self)

    def _on_button_down(self, event):
        if (
            not self._alive
        ):  # The Button-1 will still be triggered when pressing X button
            tk.Toplevel.destroy(
                self
            )  # Then this line destroys the window finally instead of the destroy() function of the base class
            return  # And finally quits the function to prevent further errors
        self._pointerdown_x = event.x
        self._pointerdown_y = event.y
        self._original_w = self.winfo_width()
        self._original_h = self.winfo_height()

    def _on_mouse_drag(self, event):
        self._dragging = True
        if not self._alive:
            return
        if (
            event.x >= self.winfo_width() - self.resize_dragwidth
            or event.y >= self.winfo_height() - self.resize_dragwidth
        ):  # If user tries to resize bot not to move the window
            self._resize(event)
        else:  # Otherwise the user must trying to drag and move the window
            self._move(event)

    def _move(self, event, coords: list = [0, 0], ignore_drag_pos_check=False):
        if event.y <= self.dragheight or ignore_drag_pos_check:
            if event.type.__str__() == "4":
                coords[0], coords[1] = event.x, event.y
            else:
                x, y = event.x - coords[0], event.y - coords[1]
                lx, ly = map(int, self.geometry().split("+")[-2:])
                self.geometry(
                    "%dx%d+%d+%d"
                    % (
                        self.winfo_width(),
                        self.winfo_height(),
                        lx + x - self._pointerdown_x,
                        ly + y - self._pointerdown_y,
                    )
                )
        else:
            if type(self.dragheight) == str:
                if self.dragheight.lower() == "full":
                    self.move(event, ignore_drag_pos_check=True)

    def _resize(self, event):
        if (
            event.x >= self.winfo_width() - self.resize_dragwidth
            and event.y >= self.winfo_height() - self.resize_dragwidth
        ):  # If dragging the right-bottom corner of the window
            self.config(cursor="sizing")
            self.int_geometry(
                event.x + self._original_w - self._pointerdown_x,
                event.y + self._original_h - self._pointerdown_y,
            )  # Then allow freely resizing the window
        elif event.x >= self.winfo_width() - self.resize_dragwidth and (
            not event.y >= self.winfo_height() - self.resize_dragwidth
        ):  # If dragging the right edge of the window
            self.config(cursor="sb_h_double_arrow")
            self.int_geometry(
                event.x + self._original_w - self._pointerdown_x, self._original_h
            )  # Then allow horizentally resizing the window
        elif (
            not event.x >= self.winfo_width() - self.resize_dragwidth
        ) and event.y >= self.winfo_height() - self.resize_dragwidth:  # If dragging the bottom edge of the window
            self.config(cursor="sb_v_double_arrow")
            self.int_geometry(
                self._original_w, event.y + self._original_h - self._pointerdown_y
            )  # Then allow veritically resizing the window

    def _on_button_release(self, event):
        self._dragging = False
        self.config(cursor="arrow")

    def make_zoomed(self):
        self._last_normal_w = self.winfo_width()
        self._last_normal_h = self.winfo_height()
        self._last_normal_x = self.winfo_x()
        self._last_normal_y = self.winfo_y()
        self.tbicon_win.state("zoomed")
        self.tbicon_win.update()
        self.int_geometry(
            self.tbicon_win.winfo_width(),
            self.tbicon_win.winfo_height() + 24,
            self.tbicon_win.winfo_x() + 8,
            self.tbicon_win.winfo_y() + 8,
        )
        self.tbicon_win.state("normal")
        self.tbicon_win.update()
        self.lift()
        self.maximize_btn["text"] = "2"
        self._is_zoomed = True

    def make_normal(self):
        self.int_geometry(
            self._last_normal_w,
            self._last_normal_h,
            self._last_normal_x,
            self._last_normal_y,
        )
        self.maximize_btn["text"] = "1"
        self._is_zoomed = False

    def toggle_normal_zoomed(self):
        if self._is_zoomed:
            self.make_normal()
        else:
            self.make_zoomed()


if __name__ == "__main__":
    from PIL import Image, ImageTk

    win = FramelessTk()
    win.mainloop()
