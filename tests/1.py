from suzaku import *

app = SkApp()
window = SkWindow(themename="dark")

SkButton(window, text="Button").vbox(padx=10, pady=10)

app.run()