#!/usr/bin/env python

import io
import socket
import struct
import numpy as np
from threading import Thread
import time                 

class FeedSocket(Thread):   

    def __init__(self,addr='raspberrypi.local',port=8000):
        Thread.__init__(self)                             
        self.addr = (addr,port)                           
        self.frame = None
        self.streaming = False

        self.sock = socket.socket()
        print("Connecting")
        self.sock.connect(self.addr)                                          
        self.conn = self.sock.makefile('rb')
        self.grabframe()        

    def grabframe(self):
        n = struct.calcsize('<L')
        sz = struct.unpack('<L',self.conn.read(n))[0]
        stream = io.BytesIO()           
        stream.write(self.conn.read(sz))
        stream.seek(0)
        self.frame = np.frombuffer(stream.read(),dtype=np.uint8)

    def run(self):
        self.streaming = True
        while self.streaming:
            self.grabframe()
        self.conn.close()
        self.sock.shutdown(1)
        self.sock.close()

    def stop(self):
        self.streaming = False
        self.join()



if __name__=='__main__':
    import cv2                                 
    feedL = FeedSocket('10.0.11.2',8000)
    feedR = FeedSocket('10.0.12.2',8000)

    # disparity range is tuned for 'aloe' image pair
    window_size = 3
    min_disp = 16
    num_disp = 112-min_disp
    stereo = cv.StereoSGBM_create(minDisparity = min_disp,
                                  numDisparities = num_disp,
                                  blockSize = 16,
                                  P1 = 8*3*window_size**2,
                                  P2 = 32*3*window_size**2,
                                  disp12MaxDiff = 1,
                                  uniquenessRatio = 10,
                                  speckleWindowSize = 100,
                                  speckleRange = 32
    )
    
    print("Starting")
    feedL.start()
    feedR.start()
    
    print("Ready")
    try:
        while feedL.is_alive():
            imgL = cv2.imdecode(feedL.frame,1)
            imgR = cv2.imdecode(feedR.frame,1)

            # img = cv.StereoBM_create(numDisparities=16, blockSize=15)
            img = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

            # https://github.com/opencv/opencv/blob/master/samples/python/stereo_match.py

            cv2.imshow("frame",img)
            cv2.waitKey(1)
    finally:
        cv2.destroyAllWindows() 
