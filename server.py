#SERVER

# -*- coding: utf-8 -*-

def URL(key, url, name, sock):   #URL命令
    if dict[name].get(key):
        sock.send(pickle.dumps(dict[name][key]))
    else:
        r = urllib.request.urlopen(url)
        sock.send(pickle.dumps(r.headers['content-length']))
        dict[name][key] = str(r.headers['content-length'])

def CMD():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--host', type=str)
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    if args.host:
        HOST = args.host
    else:
        HOST = '127.0.0.1'
    if args.port:
        PORT = args.port
    else:
        PORT = 5678
    return HOST, PORT

def SET(key, value, name):      #SET命令
    dict[name][key] = value

def GET(key,sock,name):        #GET命令
    if not dict.get(name):
        sock.send(pickle.dumps(''))
    elif not dict[name].get(key):
        sock.send(pickle.dumps(''))
    else:
        sock.send(pickle.dumps(dict[name][key]))

def function(sock, name):      #接受处理GET和SET
    while True:
        data = b''
        while True:
            temporary = sock.recv(1024)
            if temporary:
                data = data + temporary
                if len(temporary) < 1024 or len(temporary) == 1024: break
            else:
                break
        object = pickle.loads(data).split( )
        if object[0] == 'GET':
            GET(object[1],sock,name)     
        elif object[0] == 'SET':
            SET(object[1],object[2],name)
        elif object[0] == 'URL':
            URL(object[1],object[2],name,sock)

def RESIGN(sock):   #控制用户登录
    while True:
        data = b''
        while True:
            temporary = sock.recv(1024)
            if temporary:
                data = data + temporary
                if len(temporary) < 1024 or len(temporary) == 1024: break
            else:
                break
        object = pickle.loads(data)
        if re.match(r'AUTH\s.*\s.*', object):
            object = object.split()
            if resign.get(object[1]):
                if resign[object[1]] == object[2]:
                    sock.send(pickle.dumps('0'))
                    function(sock, object[1])
                else:
                    sock.send(pickle.dumps('-1'))
            else:
                sock.send(pickle.dumps('-1'))
        else:
                sock.send(pickle.dumps(''))

import socket, threading, pickle, re, argparse, urllib.request
HOST, PORT = CMD()
auth = ''
with open ('auth.conf', 'r') as f:    #读取本地注册名单
    while True:
        info = f.read(1024)
        if info:
            auth = auth + info
        else: break
dict = {}
resign = eval(auth)         #转化名单
for key in resign:          #创建用户的个人字典
    dict[key] = {}  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)
print('Waiting for connection...')
while True:                #检测用户连接
    sock, addr = s.accept()
    t = threading.Thread(target=RESIGN, args=(sock,))
    t.start()
    
