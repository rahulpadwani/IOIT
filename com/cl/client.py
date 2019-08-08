# client2.py
#!/usr/bin/env python

import socket
import cv2

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
# msg = s.recv(BUFFER_SIZE)
# if msg == 'hi' :
# msg = msg.decode('utf-8')
# print(msg)
msg=input("1-img,2-quit")
smsg=msg.encode('utf-8')
s.send(smsg)
if(msg=='1'):
    with open('received_file.jpg', 'wb') as f:
        print ('file opened')
        while True:
            #print('receiving data...')
            data = s.recv(BUFFER_SIZE)
            # print('data=%s', (data))
            if not data:
                f.close()
                print ('file close()')
                break
            # write data to a file
            f.write(data)

print('Successfully get the file')
s.close()
print('connection closed')
if msg=='1':
    img = cv2.imread('received_file.jpg',1)
    cv2.imshow('a',img)
    cv2.waitKey(0)