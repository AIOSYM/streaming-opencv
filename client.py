import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time

def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0].decode() +
                    " [" + str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)
    return img

def main():
    cap=cv2.VideoCapture(0)
    clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientsocket.connect(('192.168.100.126',8089))
    
    count = 0
    while True:
        ret,frame = cap.read()
        frame = cv2.resize(frame, (480, 320))
        #sent_time = time.time()
        #print(f'Frame #{count}: Send:{sent_time}')
        count += 1
        data = pickle.dumps(frame) 
        clientsocket.sendall(struct.pack("L", len(data))+data) 
        data = clientsocket.recv(1024)
        detections = pickle.loads(data)
        image = cvDrawBoxes(detections, frame)
        display(image)
        print('Received', repr(detections))
        
def display(frame):
    cv2.imshow("Client", frame)
    cv2.waitKey(1)

if __name__ == '__main__':
    main()
    
    
