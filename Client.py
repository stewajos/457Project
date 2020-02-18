import socket
import sys
import os
import math

HOST = 0  # The server's hostname or IP address
PORT = 0  # The port used by the server

def client():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # s.sendall(b'Connection works!')

        def connector(IP, socketPort):
            global HOST
            global PORT
            HOST = IP
            PORT = socketPort
            s.connect((HOST, PORT))

        def list():
            s.sendall(b'list')
            data = headerDecoder()
            data = s.recv(1024).decode()
            print(data)

        def retrieve(filename):
            print("retrieve")

        def store(filename):
            print("store")

        def quitty():
            print("quit")

        def headerDecoder():
            varLength = s.recv(2)
            totalLength = s.recv(varLength)
            data = s.recv(totalLength).decode()
            return data

        def headerEncoder(file):
            fileSize = os.path.getsize(file)
            fileSizeSize = math.ceil(fileSize.bit_length() / 8)
            return (fileSize, fileSizeSize)

        # def store(file, fileSize, fileSizeSize):
        #      #if fileSizeSize <= 1:
        #      #s.send(b'0')
        #      #s.sendall(bytes(str(fileSizeSize), 'utf8'))

        # fileSize, fileSizeSize = headerEncoder("client.py")
        # print("File Size Size: " + str(fileSizeSize))
        # store("client.py", fileSize, fileSizeSize)
        # print("This is what was sent " + str(sent))

        menu = 1
        while menu == 1:
            print("Menu: ")
            print("1. CONNECT <IP Address> <Server Port>")
            print("2. LIST")
            print("3. RETRIEVE <filename>")
            print("4. STORE <filename>")
            print("5. QUIT")
            print("------------------------------")

            response = input("Enter in your menu command: ").split()
            if response[0] == "CONNECT":
                connector(response[1], int(response[2]))
            elif response[0] == "LIST":
                list()
            elif response[0] == "RETRIEVE":
                retrieve(response[1])
            elif response[0] == "STORE":
                store(response[1])
            elif response[0] == "QUIT":
                menu = 0
                s.close()
            else:
                print("NOT A VALID COMMAND! ")

    #print('Received', repr(data))
    print("connect")
    return s


client()
