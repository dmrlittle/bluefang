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
async def func2():
    time.sleep(10)

    
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_640_3MG.mp4') as response:
            with open(f'/home/mrlittle/bluefang/func2','ab') as file:
                cnt=0
                async for data in response.content.iter_chunked(1024*32):
                    cnt+=1
                    print(cnt)
                    pass

            
if __name__ == '__main__':
    start = time.time()
    #func1()
    asyncio.get_event_loop().run_until_complete(main())
    print(time.time()-start)