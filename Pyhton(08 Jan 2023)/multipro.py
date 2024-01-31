from multiprocessing import *
import time

# def square(num):

#     pName = current_process().name
#     print(f"Process ID : {pName}")
#     print(f"Square of {num} is {num*num}")


# number = [1,2,3,4]
# for num in number:
#     process = Process(target=square, args=(num,))
#     process.start()


# def square(num):
#     # print(f"Square of {num} is {num*num}")
#     result = num*num
#     return num

# def using_pool(numbers):
#     start = time.time()
#     p = Pool()
#     result = p.map(square, numbers)
#     p.close()
#     end = time.time()-start
#     print(f"Pool : {end}")
 

# def without_pool(numbers):
#     result= []
#     start = time.time()   
#     for i  in numbers:
#         result.append(square(i))
#     end = time.time()-start
#     print(f"Without : {end}")


# numbers = range(4)
# without_pool(numbers)
# using_pool(numbers)

# ========================================================================================================================================================

# def add(total, l):
#     for i in range(100):
#         time.sleep(0.01)
#         lock.acquire()
#         total.value += 5
#         lock.release()

# def sub(total, l):
#     for i in range(100):
#         time.sleep(0.01)
#         lock.acquire()
#         total.value -= 5
#         lock.release

# total = Value('i', 500)
# lock = Lock()
# p1 = Process(target=add, args=(total,lock))
# p2 = Process(target=sub, args=(total,lock))

# p1.start()
# p2.start()

# p1.join()
# p2.join()

# print(total.value)

# ======================================================================================================================================================

# def square(lis, q):
#     for num in lis:
#         q.put(num*num)

# def display(q):
#     while not q.empty():
#         print(q.get())

# q = Queue()
# p2 = Process(target=display, args=(q,))
# p1 = Process(target=square, args=([1,2,3,4,5,6,7,8,9],q))

# p1.start()
# p2.start()
# p1.join()
# p2.join()

# ==========================================================================================================================================================

def sending(conn, msgs):
    for msg in msgs:
        conn.send(msg)

def recieve(conn):
    while True:
        msg = conn.recv()
        if msg == "End":
            break
        print(msg)

c1, c2=Pipe()
msgs = ["hello", "hi", "how r u?", "END"]
p1 = Process(target=sending, args=(c1,msgs))
p2 = Process(target=recieve, args=(c2,))
p1.start()
p2.start()
