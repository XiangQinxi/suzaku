from suzaku import *

app = Sk()
widget = SkWidget(app)
print(widget.winfo_x())
app.mainloop()