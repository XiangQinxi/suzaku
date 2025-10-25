import suzaku as sk
import time

def task_target(_ = None):
    global root
    print(f"Delay task executed @ {time.time()}, {round(time.time() - init_time, 3)}secs after "
           "initialization of this program.")
    root.bind("delay[5]", task_target)

root = sk.Sk()
root.bind("delay[5]", task_target)

init_time = time.time()

root.mainloop()
