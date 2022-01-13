import io
import socket
import struct
import time
from threading import Thread

class SplitFrames(object):
    '''Records video but splits at each frame                           
                                                                        
    See picamerax recipes                                               
    '''

    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length             
            # then the data                                             
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

class SocketStreamer(Thread):
    def __init__(self,camera,addr='0.0.0.0',port=8000,splitter_port=2):
        Thread.__init__(self)

        self.sock = socket.socket()
        self.sock.bind((addr,port))
        self.sock.listen(0)

        # camera.resolution = 'VGA'                                     
        # camera.framerate = 30                                         
        self.camera = camera
        # self.splitter_port = splitter_port                            
        self.streaming = False

    def run(self):
        # Wait for single connection and make a filelike object         
        conn = self.sock.accept()[0].makefile('wb')
        output = SplitFrames(conn)
        # Start recording to that connection                            
        camera.start_recording(output, format='mjpeg')
        self.streaming = True
        try:
            while self.streaming:
                self.camera.wait_recording(5)
        finally:
            # self.camera.stop_recording()                              
            self.streaming = False
            conn.write(struct.pack('<L',0))
            conn.close()

    def stop(self):
        self.streaming = False

    def join(self):
        self.sock.shutdown(1)
        self.sock.close()

class WebsocketStreamer(Thread): # TODO                                 
    pass

class ByteStreamer(Thread):     # TODO                                  
    pass

if __name__=="__main__":
    from time import sleep
    from picamerax import PiCamera

    with PiCamera(resolution='VGA', framerate=30) as camera:
        sleep(2)
        streamer = SocketStreamer(camera)
        streamer.start()
        sleep(10)
        streamer.stop()
        streamer.join()

