import socket
import threading
import time

class Tello:
    def __init__(self):
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)
        self.response_available = threading.Event() # flag to signal when the response has been received


    def send_command(self, command):

        self.response_available.clear() # reset the flag

        print('[%s] Sending command: %s to %s' % (time.ctime(), command, self.tello_ip))
        self.socket.sendto(command.encode('utf-8'), self.tello_address)

        self.response_available.wait() # block until the response has been received (TODO: Add a timeout for the request)


    def _receive_thread(self):
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                self.response_available.set() # signal that the response has been received
                print('[%s] Received from %s: %s\n' % (time.ctime(), ip, self.response))
            except socket.error as exc:
                print("Caught exception socket.error: %s" % exc)
