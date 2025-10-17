import suzaku

def output_latest_event(event: suzaku.SkEvent | None=None):
    global button
    print(f"Received event: {event.event_type}")
    latest_event = suzaku.SkEvent.global_list[-1]
    print(f"Latest event: {latest_event.event_type}")
    # button.bind("delay[2000]", output_latest_event)


root = suzaku.Sk()

button = suzaku.SkTextButton(root, text="Print latest event", command=output_latest_event).box(padx=20, pady=50)

# button.bind("delay[2]", output_latest_event)

root.mainloop()