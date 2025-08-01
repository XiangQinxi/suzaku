from suzaku import *

app = SkApp()
window = SkWindow(themename="dark")

SkButton(window, command=lambda: window.destroy()).vbox(padx=10, pady=10)
SkEntry(window, text="111111111111111").vbox(padx=10, pady=10)

app.run()