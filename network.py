import socket
import pygame
import thread
import threading

import atexit

STDPORT = ord('b') * 255 + ord('g')

class NetworkConnection():
    def __init__(self):
        self.socket = None
        self.line_ready = threading.Event()
        self.line_cleared = threading.Event()
        self.line = ""

    def _readerthread(self):
        self.socket.setblocking(True)
        c=self.socket.recv(1)   # too lazy to buffer ^^
        
        while True:
            if (c==''):
                print("connection aborted")
                self.line_ready.set()
                return

            if (c=='\n'):
                if (self.line == 'QUIT'):
                    self.socket.close()
                    self.line_ready.set()
                    return
                
                self.line_ready.set()
                print("network RECV <- : %s" % self.line)
                pygame.event.post(pygame.event.Event(pygame.USEREVENT))  # wake the pygame loop
                self.line_cleared.wait()
            else:
                self.line += c
                self.line_cleared.clear()

            c=self.socket.recv(1)

    def _listenthread(self):
        (self.socket, self.peer) = self.lsocket.accept()
        self._readerthread()

    def readline(self):
        self.line_ready.wait()
        line = self.line
        self.line = ""
        self.line_ready.clear()
        self.line_cleared.set()
        return line

    def listen(self, port=STDPORT):
        self.lsocket = socket.socket()
        self.lsocket.bind(('0.0.0.0', port))
        self.lsocket.listen(0)
        atexit.register(lambda: self.lsocket.close())
        self.thread = thread.start_new_thread(self._listenthread, ())
        
    def connect(self, address):
        self.socket = socket.create_connection(address)
        self.thread = thread.start_new_thread(self._readerthread, ())
    
    def send(self, line):
        print("network SENT -> : %s" % line)
        self.socket.send(str(line)+'\n')
        