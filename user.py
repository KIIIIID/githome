#USER

# -*- coding: utf-8 -*-

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

def receive(sock):          #接收打印服务器信息
    while True:
        data = b''
        while True:
            temporary = sock.recv(1024)
            if temporary:
                data = data + temporary
                if len(temporary) < 1024 or len(temporary) == 1024: break
            else:
                break 
        print(pickle.loads(data))
  
import socket, re, pickle, threading, time, argparse
HOST, PORT = CMD()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    #s.connect(('127.0.0.1', 5678))
    s.connect((HOST, PORT))
except socket.error:
    print('Cannot find the server')
else:
    t = threading.Thread(target=receive, args=(s,))
    t.start()
    while True:                   #检测命令格式
        commend = input('请输入:')
        if re.match(r'SET\s.*\s.*', commend) or re.match(r'GET\s.*', commend) or re.match(r'AUTH\s.*\s.*', commend) or re.match(r'URL\s.*\s.*', commend):
            s.send(pickle.dumps(commend))
            time.sleep(1)
        else:
            print('')
        
