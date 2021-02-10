# -*- coding: utf-8 -*-

import requests
from tqdm import tqdm
import multiprocessing as mp
import threading
from time import sleep
import secrets,pickle, socket, os
import configparser
import dill
import progressbar

CHUNKSIZE = 32
URL = 'http://localhost:5000'
IPV6_URL = 'https://api64.ipify.org/'
HOME_URL = f'{os.path.expanduser("~")}/.bluefang/downloads/'
PORT = 1235


manager = mp.Manager()
config = configparser.ConfigParser()
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

class Download:
    
    def __init__(self, code, url, dwnpath, lpartdict = None):
        self.code = code
        self.url = url
        self.dwnpath = dwnpath
        temp1 = int(self.head().get('Content-Length'))
        if not lpartdict:
            self.partdict = manager.list([0, 0, temp1-1, temp1])
        else:
            self.partdict = manager.list(lpartdict)
        self.name = self.partdict[0]
        
    def head(self):
        r = requests.head(self.url)
        return r.headers
    
    def start(self):
        if(self.partdict[1]>self.partdict[2]):
            print('Download Complete !')
            return 0
            
        resume_header = ({'Range': f'bytes={self.partdict[1]}-{self.partdict[2]}'})
        r = requests.get(self.url, stream=True, headers=resume_header)
        pbar = tqdm(total=self.partdict[2], initial=self.partdict[1], unit=' Bytes', )
        
        with open(f'{self.dwnpath}/{self.name}','ab') as file:
            for cnt,chunk in enumerate(r.iter_content(CHUNKSIZE*1024),1):
                self.partdict[1]+=CHUNKSIZE*1024
                self.partdict[3]-=CHUNKSIZE*1024
                file.write(chunk)
                pbar.update(CHUNKSIZE*1024)
                pickle.dump([self.code,self.url,self.dwnpath,list(self.partdict)],open(HOME_URL+self.code,'wb'))
        
        pbar.close()
                    
class Manager:
    code = None
    
    def __init__(self,dobj):
        self.url = dobj.url
        self.dobj = dobj
        
    def create(self,code):
        res=requests.post(f'{URL}/{code}/create',data=pickle.dumps([self.url]))
        if(res.ok):
            self.code=code
            print(f"Download {code} started successfully ! - {res}")
        else:
            print(f"Download {code} Failed ! - {res}")
    
    @staticmethod
    def tokgen():
        temp1 = requests.get(f'{URL}/fetchcodes')
        while True:
            tok=secrets.token_hex(6)
            if(tok not in pickle.loads(temp1.content)):
                break
        return tok
    
    def join(self,code):
        temp1 = requests.get(f'{URL}/fetchcodes')
        if(code not in pickle.loads(temp1.content)):
            print(f"Unknown {code} Failed ! - {temp1}")
        else:
            self.code=code
            print(f"Joined {code} Successfully ! - {temp1}")
    def fetch(self):
        temp1 = requests.get(f'{URL}/{self.code}/fetch')
        temp2 = pickle.loads(temp1.content)
        if(temp1.ok):
            print(f'{self.code} fetched Successfully ! - {temp1}')
        else:
            print(f'{self.code} fetch Failed ! - {temp1}')
        return sorted(temp2,key=lambda x:int(x.r.split('-')[0]))
        
    def add(self,rstart,rend):
        temp1 = requests.get(f'{IPV6_URL}').text
        temp2 = requests.post(f'{URL}/{self.code}/add/{rstart}-{rend}',pickle.dumps([temp1]))
        if(temp2.ok):
            print(f'{rstart} added Successfully ! - {temp2}')
        else:
            print(f'{rstart} add Failed ! - {temp2}')

    def delete(self,rstart,rend):
        temp1 = requests.get(f'{URL}/{self.code}/delete/{rstart}-{rend}')
        if(temp1.ok):
            print(f'{rstart} Deleted Successfully ! - {temp1}')
        else:
            print(f'{rstart} Delete Failed ! - {temp1}')
    
    def listen(self,dproc):
        print ("Socket successfully created")
        s.bind(('', PORT))
        print ("socket binded to %s" %(PORT))
        s.listen(5)   
        print ("socket is listening")
        while True:  
            c, addr = s.accept()      
            print ('Got connection from', addr ) 
            c.send(pickle.dumps(list(self.dobj.partdict)[2]))
            data = pickle.loads(c.recv(1024))
            if(data > 0):
                dproc.terminate()
                dproc = mp.Process(target=dobj.start)
                self.dobj.partdict[2] = data
                dproc.start()
            c.close()
            print ('Terminated connection from', addr )
            
    @staticmethod        
    def speak(ipv6,rmid=-1):
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.connect((ipv6, PORT, 0, 0))
        data = pickle.loads(s.recv(1024))
        s.send(pickle.dumps(rmid))
        s.close()

if __name__ == '__main__' :
    
    durl = 'https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1920_18MG.mp4'

    if(not os.path.isdir(HOME_URL)):
        os.makedirs(HOME_URL, exist_ok=True)
        
    print('Resume or Create a new download :')
    for download in os.listdir(HOME_URL):
        print(download)
    else:
        print('new')
    x = input('+>')
    if x == 'new' :
        durl = input('Download URL => ')
        temp1 = Manager.tokgen()
        dobj = Download(temp1, durl, '/home/mrlittle/bluefang')
        m = Manager(dobj)
        m.create(temp1)
        m.add(list(dobj.partdict)[0], list(dobj.partdict)[2])
    else:
        data = pickle.load(open(HOME_URL+x, 'rb'))
        dobj = Download(data[0],data[1],data[2],data[3])
        m = Manager(dobj)
        m.join(x)
        
    p1 = mp.Process(target=dobj.start)
    p2 = mp.Process(target=m.listen, args=(p1,))
    
    p1.start()
    p2.start()
        