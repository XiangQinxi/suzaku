from suzaku import *
import skia


"""    def draw(self, canvas: skia.Surface):
        rect = skia.Rect(50, 50, 90, 110)
        paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=4,
            Color=skia.ColorRED,
        )

        canvas.drawColor(skia.ColorWHITE)
        canvas.drawRect(rect, paint)

        oval = skia.RRect.MakeOval(rect)
        oval.offset(40, 60)
        paint.setColor(skia.ColorBLUE)
        canvas.drawRRect(oval, paint)

        paint.setColor(skia.ColorCYAN)
        canvas.drawCircle(180, 50, 25, paint)

        rect.offset(80, 0)
        paint.setColor(skia.ColorYELLOW)
        canvas.drawRoundRect(rect, 10, 10, paint)

        paint2 = skia.Paint()
        text = skia.TextBlob('Hello, Skia!', skia.Font(None, 18))
        canvas.drawTextBlob(text, 50, 25, paint2)"""


if __name__ == "__main__":
    appwindow = Sk(title="Suzaku GUI", background="white", size=(300, 360))
    appwindow.bind("close", lambda: print("Window closed"))

    for i in range(2):
        SkButton(appwindow, text=f"按钮 {i+1}").bind("mouse_pressed", lambda evt, i=i: print(f"Button clicked{i+1}")).vbox()
    SkLabel(appwindow, text="以下为expand=True", size=(200, 30)).vbox()
    for i in range(2, 4):
        SkButton(appwindow, text=f"按钮 {i+1}").bind("mouse_pressed", lambda evt, i=i: print(f"Button clicked{i+1}")).vbox(expand=True)
    SkLabel(appwindow, text="以上为expand=True", size=(200, 30)).vbox()
    for i in range(4, 6):
        SkButton(appwindow, text=f"按钮 {i+1}").bind("mouse_pressed", lambda evt, i=i: print(f"Button clicked{i+1}")).vbox()

    appwindow.run()
