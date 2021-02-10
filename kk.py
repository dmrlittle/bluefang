#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:23:46 2021

@author: mrlittle
"""


async def ticker(delay, to):
    for i in range(to):
        yield i
        await asyncio.sleep(delay)


async def run():
    async for i in ticker(5, 10):
        print(i)


import asyncio
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
finally:
    loop.close()