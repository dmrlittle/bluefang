#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 22:31:33 2021

@author: mrlittle
"""


import multiprocessing as mp
from time import sleep

class Test():
    
    def run(self):
        while True:
            self.pp()
            sleep(2)
            
    def pp(self):
        global ll 
        print(ll)
        
if __name__ == '__main__':
    t = Test()
    ll= 9
    p = mp.Process(target=t.run)
    p.start()
    ll=10
    