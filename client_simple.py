import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time

def main():
    
    TO_HOST = '192.168.100.126'
    PORT = 5000
    
    WIN_NAME = 'Client Display'
    CAP=cv2.VideoCapture(0)
    
    if not CAP.isOpened():
        print('Unable to connect to camera')
        sys.exit()
    
    # Create socket object using (IPv4, TCP)
    clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientsocket.connect((TO_HOST, PORT))
    
    count = 0
    while True:
        
        ret,frame = CAP.read()
        
        if not ret:
            print('Unable to read frame')
            break
        
        frame = cv2.resize(frame, (480, 320))
        data = pickle.dumps(frame) 
        
        sent_time = time.time()
        print(f'Frame#{count}:Send@{sent_time}')
        clientsocket.sendall(struct.pack("L", len(data))+data) 
        
        data = clientsocket.recv(1024)
       
        cv2.imshow(WIN_NAME, frame)
        key = cv2.waitKey(1) 
        if key == ord('q') or key == 27: #ESC_key
            print('Stop streaming')
            break
        
        count += 1
    
    cv2.destroyAllWindows() 
    clientsocket.close()
    CAP.release()
        


if __name__ == '__main__':
    main()
    
    
