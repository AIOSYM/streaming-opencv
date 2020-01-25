import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time

CAPTURE_WIDTH, CAPTURE_HEIGHT = None, None
DAKRNET_WIDTH, DARKNET_HEIGHT = 416, 416

def convertBack(x0, y0, w0, h0):
    
    WIDTH_RATIO, HEIGHT_RATIO = CAPTURE_WIDTH/DAKRNET_WIDTH, CAPTURE_HEIGHT/DARKNET_HEIGHT
    x, y, w, h = x0*WIDTH_RATIO, y0*HEIGHT_RATIO, w0*WIDTH_RATIO, h0*HEIGHT_RATIO
    
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

def cvDrawBoxes(detections, frame):
    img = frame
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
    
    global CAPTURE_WIDTH, CAPTURE_HEIGHT
    
    TO_HOST = '192.168.100.126'
    PORT = 5000
    
    SENT_WIN_NAME = 'Client SENT'
    RECEIVED_WIN_NAME = 'Client RECEIVED'
    
    CAP = cv2.VideoCapture(0)
    CAPTURE_WIDTH = CAP.get(cv2.CAP_PROP_FRAME_WIDTH)
    CAPTURE_HEIGHT = CAP.get(cv2.CAP_PROP_FRAME_HEIGHT)
     
    if not CAP.isOpened():
        print('Unable to connect to camera')
        sys.exit()
    
    # Create socket object using (IPv4, TCP)
    clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientsocket.connect((TO_HOST, PORT))
    
    count = 0
    while True:
        
        ret,frame = CAP.read()
        frame_copy = np.copy(frame)
                
        if not ret:
            print('Unable to read frame')
            break
        
        frame = cv2.resize(frame, (416, 416))
        data = pickle.dumps(frame) 
        
        # Sent timestamp------
        sent_time = time.time()
        print(f'Frame#{count}:Sent@{sent_time}')
        #---------------------------------
        try:
            clientsocket.sendall(struct.pack("L", len(data))+data) 
            data = clientsocket.recv(1024)
            detections = pickle.loads(data)
            
            # Received back timestamp------
            received_time = time.time()
            print(f'Frame#{count}:ReceivedBack@{received_time}')
            #---------------------------------
        except Exception as e:
            print('Disconnected from server')
            break
                
        bbox_frame = cvDrawBoxes(detections, frame_copy)
        #cv2.imshow(SENT_WIN_NAME, frame_copy)
        cv2.imshow(RECEIVED_WIN_NAME, bbox_frame)
        
        key = cv2.waitKey(1) 
        if key == ord('q') or key == 27: #ESC_key
            print('Stop streaming')
            break
        
        count += 1
        
if __name__ == '__main__':
    main()
    
    
