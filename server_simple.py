import socket
import sys
import cv2
import pickle
import numpy as np
import struct 
import time

def main():

    # CHANGE THIS TO MATCH SERVER IP
    HOST = '127.0.0.1' #LOCAL_HOST
    PORT = 5000
    
    WIN_NAME = 'Server Display'

    serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')

    serversocket.bind((HOST,PORT))
    print('Socket bind complete')
    serversocket.listen(10)
    print('Socket now listening')

    conn,addr = serversocket.accept()

    data = b''
    payload_size = struct.calcsize("L") 
    count = 0
    while True:
        
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        
        sent_time = time.time()
        print(f'Frame#{count}:Received@{sent_time}')
        cv2.imshow(WIN_NAME,frame)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            print('Server is closed.')
            break
        
        count += 1
        
    cv2.destroyAllWindows()
    serversocket.close()
    
if __name__ == '__main__':
    main()
