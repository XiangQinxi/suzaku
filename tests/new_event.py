import suzaku as sk


root = sk.Sk(is_get_context_on_focus=False)

button = sk.SkTextButton(
    root, text="Print latest event", command=lambda: print(sk.SkEvent.latest.event_type)
).box(padx=20, pady=50)
button = sk.SkTextButton(
    root, text="Print RAM-draining stuff", command=lambda: print("Not implemented")
).box(padx=20, pady=50)

root.mainloop()
