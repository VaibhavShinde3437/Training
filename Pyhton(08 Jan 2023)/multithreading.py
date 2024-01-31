from threading import *
from time import *

# def display():
#     for _ in range(10):
#         print("Hello")
#         sleep(0.5)

# t1 = Thread(target=display)
# t1.daemon = True
# t1.start()
# sleep(2)
# print("Stop")

# =========================================================================================================================================================

# def task():
#     for _ in range(5):
#         print("Task")

# t1 = Timer(5,task)
# t1.start()

# for _ in range(5):
#     print("Main")

# ==========================================================================================================================================================

# threads = ["Thread-1", "Thread-2", "Thread-3", "Thread-4"]
# barrier = Barrier(len(threads))
# def display(name):
  
#     print(f"{name} started")
#     barrier.wait()
#     print(f"{name} Stopped")




# for name in threads:
#     thread = Thread(target=display, args=(name,))
#     thread.start()
    