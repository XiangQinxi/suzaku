from suzaku import *
import time

root = Sk()

progress = SkProgressBar(root).grid(row=0, column=0, columnspan=3, padx=5, pady=5)


def start(event=None):
    progress.configure(value=progress.cget("value") * 1.1 + 1)
    progress.update(True)
    if progress.cget("value") < progress.cget("maxvalue"):
        root.bind("delay[100ms]", start)


button = SkTextButton(
    root, text="Increase", command=lambda: progress.configure(value=progress.cget("value") + 10)
).grid(row=1, column=0, padx=5, pady=5)

button2 = SkTextButton(
    root, text="Decrease", command=lambda: progress.configure(value=progress.cget("value") - 10)
).grid(row=1, column=1, padx=5, pady=5)

button3 = SkTextButton(root, text="Start", command=lambda: start()).grid(
    row=1, column=2, padx=5, pady=5
)

root.mainloop()
