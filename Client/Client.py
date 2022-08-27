import sys
sys.path.insert(1,'..')
from Common_Class import *

import json
import socket as sock

#Class used for managing the client
class Client:
    sock = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)  # socket create
    server_address = ('localhost', 10000)
    #client initialization
    def __init__(self):
        print("Pietro Tellarini's Project: Client\n")
        m = Message()
        while True:
            inp = input()
            if inp == 'help':
                print('These are the three commands:\n\n'+
                      "'list' : for for having the list of files available to download from the server\n\n"+
                      "'get' : to receive a file from the server\n"+
                      "    get filename filepath(nothing for saving the file is in the same folder of the program)\n\n"+
                      "'put' : to upload a file to the server\n"+
                      "     put filename filepath(nothing in case the file is in the same folder of the program)\n\n"+
                      "'quit' : to close the program")
            elif inp == 'list':
                m.command_list(self.sock, self.server_address)
                packet, address = self.sock.recvfrom(8192)
                packet = json.loads(packet.decode())
                if packet[0] == 'SEND':
                    for i in packet[1]:
                        print(" {} -" .format(i), end = "")
                    print()
                else:
                    print(packet[1])
            elif inp[:3] == 'get':
                l = inp.split(" ")
                filename = l[1]
                print(filename)
                m.command_get(self.sock, self.server_address, filename)
                r = m.receive(self.sock)
                if r[1] == 0:
                    if len(l) == 3:
                        filename = l[2] + "/" + l[1]
                    m.save_file(filename, r[0])
                else:
                    print(r[0])
            elif inp[:3] == 'put':
                l = inp.split(" ")
                if len(l) == 3:
                    filepath = l[2] + "/" + l[1]
                elif len(l) == 2:
                    filepath = l[1]
                m.command_put(self.sock, self.server_address, l[1], filepath)
            elif inp == 'quit':
                self.sock.close()
                break
            else:
                print("write 'help' for knowing how it works the program or 'quit' to close it\n")



#main
c = Client()

