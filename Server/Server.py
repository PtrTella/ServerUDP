import sys
sys.path.insert(1,'..')
from Common_Class import *

import socket as sock
import os
import json

#Class to initialize the server
class Server:
    server_address = ('localhost', 10000)
    socket = None

    #inizialization
    def __init__(self):
        print("Pietro Tellarini's Project: Server\n")
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)            #UDP socket creation
        self.socket.bind(self.server_address)

        while True:                                                         #thread for listening
            print('\n\r waiting to receive message...\n')
            packet, address = self.socket.recvfrom(8192)
            packet = json.loads(packet.decode())
            header = packet[0]
            data = packet[1]
            if (header == "LIST"):
                print(self.get_files_list())
                p = Packet('SEND', self.get_files_list())
                try:
                    self.socket.sendto(p.get(), address)
                except Exception as info:
                    self.socket.sendto(Packet('ERR', str(info)).get(), address)
                    print(info)
            elif(header == "GET"):
                message = Message()
                try:
                    message.read_file(data)
                    message.send_file(self.socket, address)
                except Exception as info:
                    self.socket.sendto(Packet('ERR', str(info)).get(), address)
                    print(info)
            elif(header == "PUT"):
                filename = data
                message = Message()
                r = message.receive(self.socket)
                if r[1] == 0:
                    message.save_file(filename, r[0])
                else:
                    print(r[0])

    def get_files_list(self):
        clean = ['Server.py']
        l = os.listdir()
        for ob in clean:
            if ob in l:
                l.remove(ob)
        return l

#main
s = Server()