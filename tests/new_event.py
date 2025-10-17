import suzaku as sk


def output_latest_event(event: sk.SkEvent | None = None):
    global button
    print(f"Received event: {event.event_type}")
    latest_event = sk.SkEvent.global_list[-1]
    print(f"Latest event: {latest_event.event_type}")
    # button.bind("delay[2000]", output_latest_event)


root = sk.Sk(is_get_context_on_focus=False)

button = sk.SkTextButton(
    root, text="Print latest event", command=output_latest_event
).box(padx=20, pady=50)
print(root.get_widget_with_id("SkAppWindow0.SkTextButton2"))

# button.bind("delay[2]", output_latest_event)

root.mainloop()
