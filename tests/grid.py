from suzaku import *

root = Sk()

for row in range(5):
    for col in range(5):
        text = f"{row},{col}"
        if row == 0 and col == 0:
            text = "Start"
        if row == 4 and col == 4:
            text = "End"
        padx = 5
        pady = 5
        if row == 2 and col == 2:
            padx = 10
            pady = 10
        SkTextButton(root, text=text).grid(row=row, column=col, padx=padx, pady=pady)


root.mainloop()
