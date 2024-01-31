import asyncio
import time

# start = time.time()

# async def buy():
#     await asyncio.sleep(7)
#     print("Bought something")

# async def insta():
#     await asyncio.sleep(3)
#     print("Scroll insta")

# async def main():
#     # await insta()
#     # await buy()
#     t1 = asyncio.create_task(insta())
#     t2 = asyncio.create_task(buy())
#     await asyncio.gather(t1,t2)

# asyncio.run(main())

# print(time.time()-start)

# ===========================================================================================================================================================

start = time.time()
async def fetch():
    print("started fetching")
    await asyncio.sleep(1)
    print("fetching done")

async def main():
    print("Starting main")
    t1 = asyncio.create_task(fetch())
    t2 = asyncio.create_task(fetch())
    t3 = asyncio.create_task(fetch())

    await asyncio.gather(t1,t2,t3)

    print("Main completed")
    print(time.time()-start)

asyncio.run(main())