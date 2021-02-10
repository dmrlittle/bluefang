
import requests
from tqdm import tqdm
import multiprocessing as mp
import threading
from time import sleep
import json,secrets

CHUNKSIZE = 32
manager = mp.Manager()
partdict = manager.dict({})

def origincheck(func):
        def inner(self, *args, **kwargs):
            r = requests.head(self.url)
            if(r.headers.get('Accept-Ranges') == 'bytes'):
                return func(self, *args, **kwargs) 
            else:
                print('Origin Check Failed !')
        return inner
    
class Download:
    
    def __init__(self, url, dwnpath):
        self.url = url
        self.dwnpath = dwnpath
        
        temp1=int(self.head().get('Content-Length'))
        del temp1

    def head(self):
        r = requests.head(self.url)
        return r.headers
    
    def start(self):
        r = requests.get(self.url, stream=True)
        
        with open(f'{self.dwnpath}/{self.name}','wb') as file:
            for cnt,chunk in tqdm(enumerate(r.iter_content(CHUNKSIZE*1024),1)):
                file.write(chunk)
                self.cache_headers.update(rans=cnt*1024*CHUNKSIZE)
                self.rangeupdater(self.start)
                
    def resume(self):
        r = requests.get(self.url, stream=True, headers=self.resume_headers)
        
        with open(f'{self.dwnpath}/{self.name}','ab') as file:
            for cnt,chunk in tqdm(enumerate(r.iter_content(CHUNKSIZE*1024),1)):
                file.write(chunk)
                self.cache_headers.update(rans=cnt*1024*CHUNKSIZE)
            
class Boss:
    
    def __init__(self,dobj):
        self.dobj=dobj
    
    def seek(self):
        return json.dumps(self.dobj.partdict).encode()
        
    def tell(self,partdict):
        self.dobj.partdict=partdict
        
    def create(self,partdict=None):
        global partdict
        if(not partdict):
            rend=int(self.dobj.head().get('Content-Length'))
            tok=secrets.token_hex(6)
            self.dobj.name=tok
            partdict.update({tok:[0,0,rend,rend]})
        else:
            tok=secrets.token_hex(6)
            while(True):
                if(tok in partdict):
                    continue
                self.dobj.name=tok
                partdict=self.donna(tok,partdict)
                
    def donna(tok,partdict):
        temp1=sorted(partdict.items(),key=lambda x:x[1][1])[0]
        temp2=temp1[1][0]+int((temp1[1][1]-temp1[1][0])/2)
        temp3=temp2-temp1[1][0]+1
        partdict.update({temp1[0]:[[temp1[1][0],temp2-1],temp3]})
        partdict.update({tok:[[temp2,temp1[1][1]],temp3]})
        return partdict
    
    
class PartitionController:
    part={}
    
    def __init__(self,headers):
        self.headers=headers
        
    def check(func):
        def inner(self,*args,**kwargs):
            if(self.headers.get('Accept-Ranges') == 'bytes'):
                return func(self, *args, **kwargs) 
            else:
                print('Origin Check Failed !')
        return inner
    
    @check
    def assign():
        pass
        
d=Download('testing001.mp4','https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_640_3MG.mp4','/home/mrlittle/bluefang')
        