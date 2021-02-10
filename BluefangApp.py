p# -*- coding: utf-8 -*-

import requests
from tqdm import tqdm
import multiprocessing
import threading
from time import sleep

CHUNKSIZE = 32

class Download:
    status={}
    cache_headers = {'rans':0 ,'rane':1}
    temp_headers = {'rans':0 ,'rane':1}
    resume_headers = {'Range': 'bytes='+str(cache_headers['rans'])+'-'+str(cache_headers['rane'])}
    
    def __init__(self, name, url, dwnpath):
        self.name = name
        self.url = url
        self.dwnpath = dwnpath
        
    def origincheck(func):
        def inner(self, *args, **kwargs):
            r = requests.head(self.url)
            if(r.headers.get('Accept-Ranges') == 'bytes'):
                return func(self, *args, **kwargs) 
            else:
                print('Origin Check Failed !')
        return inner
    
    def cachecheck(func):
        def inner(self, *args, **kwargs):
            if(self.cache_headers['rans'] < self.cache_headers['rane']):
                return func(self,*args, **kwargs)
            else:
                print('Cache Check Failed !')
        return inner

    def rangeupdater(self,func):
        print(str(self.temp_headers['rane'])+"  ||||||||||||  "+str(self.cache_headers['rane']))
        if(self.temp_headers['rane']==self.cache_headers['rane']):
            pass
        else:
            print('hi')
            self.temp_headers['rane']=self.cache_headers['rane']
            return func
        
    @cachecheck
    @origincheck
    def start(self):
        
        r = requests.get(self.url, stream=True)
        
        with open(f'{self.dwnpath}/{self.name}','wb') as file:
            for cnt,chunk in tqdm(enumerate(r.iter_content(CHUNKSIZE*1024),1)):
                file.write(chunk)
                self.cache_headers.update(rans=cnt*1024*CHUNKSIZE)
                self.rangeupdater(self.start)
    
    @cachecheck
    @origincheck
    def resume(self):
        r = requests.get(self.url, stream=True, headers=self.resume_headers)
        
        with open(f'{self.dwnpath}/{self.name}','ab') as file:
            for cnt,chunk in tqdm(enumerate(r.iter_content(CHUNKSIZE*1024),1)):
                file.write(chunk)
                self.cache_headers.update(rans=cnt*1024*CHUNKSIZE)
    
    def partition(self,rane):
        self.cache_headers.update(rane=rane)
        

d=Download('testing001.mp4','https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_640_3MG.mp4',
           '/home/mrlittle/bluefang')

#d.start()
        