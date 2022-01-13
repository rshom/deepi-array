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


class CtlSocket():                             
    pass                                       

if __name__=='__main__':                       
    import cv2                                 
    feed1 = FeedSocket('10.0.11.2',8000)
    feed2 = FeedSocket('10.0.12.2',8000)
    print("Starting")
    feed1.start()
    feed2.start()
    print("Ready")
    stereo = cv2.StereoBM_create()
    try:
        while True:
            img1 = cv2.imdecode(feed1.frame,1)
            img2 = cv2.imdecode(feed2.frame,1)
            # img3 = cv2.imdecode(feed1.frame,1)
            # img4 = cv2.imdecode(feed2.frame,1)

            # Post processing/compilation
            
            # img = np.vstack([np.hstack([img1, img2]),
            #                  np.hstack([img3, img4])])

            gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

            disparity = stereo.compute(gray1,gray2).astype(np.float32)/16

            cv2.imshow("Disparity",disparity)
            if cv2.waitKey(1) == 27:
                # close out on escape
                break

    finally:
        feed1.stop()
        feed2.stop()
        cv2.destroyAllWindows() 
