# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
import multiprocessing as mp
import threading as td
from time import sleep

import secrets,pickle, socket, os, signal
import configparser
import dill
import progressbar
import select
import dill

CHUNKSIZE = 32
URL = 'http://localhost:5000'
IPV6_URL = 'https://api64.ipify.org/'
HOME_URL = f'{os.path.expanduser("~")}/.bluefang/downloads1/'
PORT = 11290

    
class Downloader():
    dcheck = False
    
    def __init__(self, code, url, dwnpath, partdict = None):
        self.code = code
        self.url = url
        self.dwnpath = dwnpath
        assert self.check(), 'Check Internet Connection !'
        self.ignition(partdict)
        
    def check(self):
        self.headers = requests.head(self.url).headers
        self.length = int(self.headers.get('Content-Length'))
        return self.length
        
    def ignition(self, partdict = None):
        if partdict :
            self.partdict = partdict
        else:
            self.partdict = [0, 0, self.length-1, self.length]
        self.name = self.partdict[0]
        
    def save(self):
        #pickle.dump([self.code,self.url,self.dwnpath,list(self.partdict)],open(HOME_URL+self.code,'wb'))
        Manager.backup(dobjs, 'dobjs')
        
    def start(self):
        global _dcheck
        if(self.partdict[1]>self.partdict[2]):
            return 0
        
        resume_header = ({'Range': f'bytes={self.partdict[1]}-{self.partdict[2]}'})
        r = requests.get(self.url, stream=True, headers=resume_header)
        pbar = tqdm(total=self.partdict[2], initial=self.partdict[1], unit=' Bytes', )
        
        with open(f'{self.dwnpath}/{self.name}','ab') as file:
            for chunk in r.iter_content(CHUNKSIZE*1024):
                if self.dcheck :
                    self.dcheck = False
                    print('Terminated')
                    return
                self.partdict[1]+=len(chunk)
                self.partdict[3]-=len(chunk)
                file.write(chunk)
                self.save()
                pbar.update(len(chunk))
        pbar.close()
        
class TCPConnector():
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.port = PORT
        
    def listen(self, n_cli = 5):
        def inner(self, n_cli):
            self.sock.bind(('', self.port))
            self.sock.listen(n_cli)
            print ("socket is listening")
            while True:
                c_sock, addr = self.sock.accept()      
                print ('Got connection from', addr )
                code = pickle.loads(c_sock.recv(1024))
                dobj = dobjs.get(code)
                if dobj: 
                    c_sock.send(pickle.dumps(list(dobj.partdict)))
                    data = pickle.loads(c_sock.recv(1024))
                    if(data > 0):
                        print('Process Restart !')
                        if dobj.dcheck:
                            Manager.dwnload_kill(code)
                            dobj.partdict[2] = data
                            dobj.partdict[3] = dobj.partdict[2] - dobj.partdict[1]
                            Manager.dwnload_strt(code)
                        else:
                            dobj.partdict[2] = data
                            dobj.partdict[3] = dobj.partdict[2] - dobj.partdict[1]
                c_sock.close()
                print ('Terminated connection from', addr )
        td.Thread(target = inner, args = (self,n_cli,), daemon = True).start()
        
    def speak(self, ipv6, code, rmid=-1):
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as sock:
            sock.connect((ipv6, self.port, 0, 0))
            sock.send(pickle.dumps(code))
            data = pickle.loads(sock.recv(1024))
            sock.send(pickle.dumps(rmid))
        return data
        
        
class Manager():
    global dobjs
    
    pobjs = {}
    dobjs = {}
    apiobjs = {}
    peerdict = {}
    
    def __init__(self, tcpobj):
        self.tcpobj = tcpobj
        self.loader()
        
    def loader(self):
        files=[file for file in os.listdir(HOME_URL)]
        if 'apiobjs' in files:
            self.apiobjs = pickle.load(open(HOME_URL+'apiobjs', 'rb'))
        if 'dobjs' in files:
            dobjs_red = pickle.load(open(HOME_URL+'dobjs', 'rb'))
            [ dobjs.update({code:Downloader(code,*args)}) for code, *args in dobjs_red ]
        
    def on_start(self):
        self.tcpobj.listen()
        
    @staticmethod
    def dwnload_strt(code):
        td.Thread(target=dobjs[code].start, daemon = True).start()
    
    @staticmethod       
    def dwnload_kill(code):
        if not dobjs[code].dcheck:
            dobjs[code].dcheck = True
            print('Terminated')
    
    def new(self, url, dwnpath, partdict=None):
        apiobj = APIHandler(url)
        code = apiobj.create()
        self.apiobjs[code] = apiobj
        dobjs[code] = Downloader(code, url, dwnpath)
        apiobj.add(dobjs[code].partdict[0],dobjs[code].partdict[2])
        Manager.backup(dobjs, 'dobjs')
        Manager.backup(self.apiobjs, 'apiobjs')
        return code
        
    def join(self, code):
        apiobj = APIHandler()
        code = apiobj.join(code)
        self.apiobjs[code] = apiobj

    def fetch(self, code):
        apiobj = self.apiobjs.get(code)
        self.peerdict[code] = apiobj.fetch()
    
    def share(self, code, peer, rmid):
        apiobj = self.apiobjs.get(code)
        rstart, rend = peer[1]
        self.tcpobj.speak(peer[0], code, rmid)
        apiobj.modify(rstart, rend, rmid)
        aptobj.add(rmid+1, rend)
        
    @staticmethod
    def backup(obj, hdr):
        if(not os.path.isdir(HOME_URL)):
            os.makedirs(HOME_URL, exist_ok=True)
        if hdr == 'apiobjs' :
            pickle.dump(obj ,open(HOME_URL+hdr,'wb'))
        elif hdr == 'dobjs' :
            obj_red = [(code, dobj.url, dobj.dwnpath, list(dobj.partdict)) for code,dobj in obj.items()]
            pickle.dump(obj_red, open(HOME_URL+hdr,'wb'))

class APIHandler():
    
    def __init__(self, url = None, code = None):
        self.code= code
        self.url = url
        
    def create(self):
        res = requests.post(f'{URL}/create', data = pickle.dumps([self.url]))
        if(res.ok):
            self.code = pickle.loads(res.content)
            print(f"Download {self.code} started successfully ! - {res}")
        else:
            self.code = None
            print(f"Download {self.code} Failed ! - {res}")
        return self.code
    
    def join(self, code):
        res = requests.get(f'{URL}/join/{code}')
        if(res.ok):
            self.code = pickle.loads(res.content)
            print(f"Joined {self.code} Successfully !")
        else:
            self.code = None
            print(f"Join {self.code} Failed !")
        return self.code
    
    def fetch(self):
        res = requests.get(f'{URL}/fetch/{self.code}')
        if(res.ok):
            data = pickle.loads(res.content)
            print(f'{self.code} fetched Successfully ! - {res}')
        else:
            print(f'{self.code} fetch Failed ! - {res}')
        return sorted(data, key=lambda x:int(x[1][0]))
        
    def add(self, rstart, rend):
        ipv6 = APIHandler.get_ipv6()
        res = requests.post(f'{URL}/add/{self.code}', data = pickle.dumps([ipv6, (rstart, rend)]))
        if(res.ok):
            print(f'{rstart} added Successfully ! - {res}')
        else:
            print(f'{rstart} add Failed ! - {res}')
            
    def modify(self, rstart, rend, rnewend):
        res = requests.post(f'{URL}/modify/{self.code}', data = pickle.dumps([(rstart, rend, rnewend)]))
        if(res.ok):
            print(f'{rstart} added Successfully ! - {res}')
        else:
            print(f'{rstart} add Failed ! - {res}')
        
    def delete(self, rstart, rend):
        res = requests.post(f'{URL}/delete/{self.code}', data = pickle.dumps([(rstart, rend)]))
        if(res.ok):
            print(f'{rstart} Deleted Successfully ! - {temp1}')
        else:
            print(f'{rstart} Delete Failed ! - {temp1}')
            
    def drop(self):
        res = requests.get(f'{URL}/drop/{self.code}')
        if(res.ok):
            print(f"Droped {code} Successfully !")
        else:
            print(f"Drop {code} Failed !")
            
    @staticmethod
    def get_ipv6():
        try:
            with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as sock:
                sock.connect(("2001:4860:4860::8888", 80, 0, 0))
                ip_addr = sock.getsockname()[0]
            return ip_addr
        except Exception as e:
            return None
        
if __name__ == '__main__' :
    
    durl = 'https://file-examples-com.github.io/uploads/2018/04/file_example_MOV_1920_2_2MB.mov'
    dwnpath = '/home/mrlittle/bluefang'
    
    tcpobj = TCPConnector()
    manobj = Manager(tcpobj)