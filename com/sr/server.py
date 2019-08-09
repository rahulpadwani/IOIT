# server2.py
import socket
from threading import Thread
from socketserver import ThreadingMixIn

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for "+ip+":"+str(port))

    def run(self):
        self.communicate()

    def communicate(self):
        msg=''
        flag="connected"
        while flag != "exit":
            menu="1:-find person\n2:-set data\n3:-get data\n4:-quit"
            msg=menu.encode('utf-8')
            self.sock.send(msg)
            msg=self.sock.recv(BUFFER_SIZE)
            msg=msg.decode('utf-8')
            print(msg)
            # call functions here---
            if msg == '1':
                response='finding person'
                msg=response.encode('utf-8')
                self.sock.send(msg)
            elif msg =='2':
                response='reciving data'
                msg=response.encode('utf-8')
                self.sock.send(msg)
            elif msg =='3':
                response='sending data'
                msg=response.encode('utf-8')
                self.sock.send(msg)
                self.send_img()
                flag="exit"
            elif msg =='4':
                response='closing connection'
                msg=response.encode('utf-8')
                self.sock.send(msg)
                flag="exit"
            else :
                response='invalid'
                msg=response.encode('utf-8')
                self.sock.send(msg)
                
            
        self.sock.close()

    def send_img(self):
        filename='img.jpg'
        f = open(filename,'rb')
        print ("file opened")
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                # print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break
    def get_img(self):
        with open('received_file.jpg', 'wb') as f:
            print ('file opened')
            while True:
                #print('receiving data...')
                data = self.sock.recv(BUFFER_SIZE)
                # print('data=%s', (data))
                if not data:
                    f.close()
                    print ('file close()')
                    break
                # write data to a file
                f.write(data)


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)
    


for t in threads:
    t.join()
