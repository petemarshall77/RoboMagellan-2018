from socket import socket, AF_INET, SOCK_STREAM

# MONTY III Camera interface
#   Input - data from processing (blurry_blobs_n.pde)
#   Output - XValue in frame, +/- from center, number of bloxels
#            (pixels) in biggest blurry_blobs_n

class Camera:

    def __init__(self, port_num, logger):
        self._running = False
        self.logger = logger
        self.logger.write("Camera: starting")
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(('localhost', port_num))
        self.blob_location = 0 # TODO - fix this awful name!
        self.blob_size = 0

    def terminate(self):
        self._running = False
        
    def get_blob_info(self):
        return (int(self.blob_location), int(self.blob_size))

    def run(self):
        self._running = True
        self.logger.write("Camera: running")
        while(self._running == True):
            data = self.socket.recv(8192)
            try:
                self.blob_location = data.split(',')[0]
                self.blob_size = data.split(',')[1]
            except:
                self.logger.write("Camera: bad camera data: %s" % data)
                self.blob_location = 0
                self.blob_size = 0

        self.socket.close()
        self.logger.write("Camera: terminated")
