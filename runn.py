# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import requests, time
from tqdm import tqdm



def func1():
    r = requests.get('https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_640_3MG.mp4', stream=True)
    with open(f'/home/mrlittle/bluefang/func1','ab') as file:
        for cnt,chunk in tqdm(enumerate(r.iter_content(320*1024),1)):
            file.write(chunk)
            
    
async def func2(queue):
    while True:
        print(await queue.get())


async def func3():
    for i in range(20):
        print(i)
        await queue.put(i*100)
        await asyncio.sleep(5)
        print('jo')
        yield(i)
        await asyncio.sleep(5)
        print('ji')

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_480_1_5MG.mp4') as response:
            with open(f'/home/mrlittle/bluefang/func2','ab') as file:
                tasks=[]
                cnt=0
                gen = func3()
                assert gen.__aiter__() is gen
                asyncio.ensure_future(func2(queue))
                for i in range(5):
                    await gen.__anext__()


            
if __name__ == '__main__':
    queue = asyncio.Queue()
    start = time.time()
    #func1()
    asyncio.get_event_loop().run_until_complete(main())
    print(time.time()-start)
