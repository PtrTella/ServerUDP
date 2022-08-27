import base64
import json
import hashlib

#class used by the Server and the Client to speak
class Message:
    message = None
    def __init__(self):
            self.message = None

    #method used to read the file
    def read_file(self, filename):
        with open(filename, 'rb') as f:
            file = f.read()
            file = base64.b64encode(file).decode()
            f.close()
        self.message = file

    #method used to save the file
    def save_file(self, filename, file):
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(file.encode()))
            f.close()

    #method used to send the file
    def send_file(self, socket, address):
        buffer = 8000
        while len(self.message) > 0:
            hasher = hashlib.md5()
            hasher.update(self.message.encode())
            while len(self.message) > 0:
                p = Packet('SEND', (self.message[:(buffer - 40)])).get()  # sending chunks of the message inside packets
                socket.sendto(p, address)
                self.message = self.message[buffer - 40:]
            socket.sendto(Packet("END", hasher.hexdigest()).get(),
                          address)  # sending the last packet, header_type 'END'
            print("message sent")

    #method used to receive the file
    def receive(self, socket):
        message = "";
        while True:  # receiving packets with header_type 'SEND'
            data, address = socket.recvfrom(8192)  # until he does receive last packet with header_type 'END'
            packet = json.loads(data.decode('utf8'))
            if packet[0] == 'ERR':
                return packet[1], 1  # returns a error if there problems detected by the sender
            elif packet[0] == 'END':
                break  # that can be for example: the file required does not exist
            message += packet[1]

        hasher = hashlib.md5()
        hasher.update(message.encode())
        if hasher.hexdigest() != packet[1]:
            print("file wrongly received")  # returns a error if the checksum fails
            socket.sendto(Packet('END', 'checksum failed').get(), address)
            return "checksum failed", 1
        print("file correctly received")
        socket.sendto(Packet('END', 'ok').get(), address)
        return message, 0

    #method used to start the client-server communication with the command list
    def command_list(self, socket, address):
        p = Packet('LIST', '')
        try:
            socket.sendto(p.get(), address)
        except Exception as info:
            print(info)

    # method used to start the client-server communication with the command get
    def command_get(self, socket, address, filename):
        try:
            socket.sendto(Packet('GET', filename).get(), address)  # sends to the server the packet with header_type Get, content the filename
        except Exception as info:
            print(info)

        print('\nwaiting to receive files..\n')

    # method used to start the client-server communication with the command put
    def command_put(self, socket, address, filename, filepath):
        try:
            socket.sendto(Packet('PUT', filename).get(), address)
            self.read_file(filepath)
            try:
                self.send_file(socket, address)
                packet, address = socket.recvfrom(8192)
                packet = json.loads(packet.decode())
                if (packet[0] == 'END'):
                    print(packet[1])
            except Exception as info:
                print(info)
        except Exception as info:
            print(info)


    def toString(self):
        return self.message

#Class to create packet objects
class Packet:
    header = None
    data = None

    def __init__(self, header, data):
        self.header = self.header_create(header)
        self.data = self.data_create(data)
    def header_create(self, header):
        return header
    def data_create(self, data):
        return data

    def get(self):
        return json.dumps([self.header, self.data]).encode()
