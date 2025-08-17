from suzaku import *


app = SkApp()

win = SkWindow()

btn = SkTextButton(win, text="Test")
btn.box()
btn.after(2, lambda: btn.config(text="Test2"))

message = """
1234
14321
"""

label = SkText(win, text=message)
label.box()

app.mainloop()