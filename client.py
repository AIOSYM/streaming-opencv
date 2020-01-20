import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time

def main():
    cap=cv2.VideoCapture(0)
    clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientsocket.connect(('localhost',8089))
    
    count = 0

    while True:
        ret,frame = cap.read()
        frame = cv2.resize(frame, (480, 320))
        display(frame)
        sent_time = time.time()
        print(f'Frame #{count}: Send:{sent_time}')
        count += 1
        data = pickle.dumps(frame) 
        clientsocket.sendall(struct.pack("L", len(data))+data) 
        
def display(frame):
    cv2.imshow("Client", frame)
    cv2.waitKey(1)

if __name__ == '__main__':
    main()
    
    