# import socket
# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(2)
#             #print("Server data print out: " + str(data))
#             #data2 = conn.recv(1024)
#             strings = str(data, 'utf8')
#             print(strings)
#             num = int(strings)
#             print("Final Number or something: " + str(num))
#             if not data:
#                 break
#             conn.sendall(data)
#             #conn.sendall(data2)

import sys
import socket
import selectors
import traceback
import os
import math
import pickle

hostname = socket.gethostname()
IP = '127.0.0.1' #socket.gethostbyname(hostname)
port = 42069


class Server(object):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((IP, port))
        sock.listen()
        conn, addr = sock.accept()
        print("server listening on: ", port)
        print("servers address: ", IP)
        # listen for connection for client

        with conn:
            print('connected by', addr)

            def listen(self):
                self.sock.listen(5)
                while True:
                    client, address = self.sock.accept()
                    print("connection made with: " + str(address))

            def listentoclient(self, client, address):

                def headerDecoder(s):
                    varLength = s.recv(2)
                    totalLength = s.recv(varLength)
                    data = s.recv(totalLength)
                    return data

                def headerEncoder(file, s):
                    fileSize = os.path.getsize(file)
                    fileSizeSize = math.ceil(fileSize.bit_length() / 8)
                    s.send(fileSizeSize)
                    s.send(fileSize)
                    return (fileSize, fileSizeSize)

                def sendFile(file, conn):
                    f = open(file, 'rb')
                    l = f.read(os.path.getsize(file))
                    conn.send(l)
                    f.close()

                def listtostring(sock):
                    str = ""
                    for element in sock:
                        str += " " + element
                    return str

                # def list(conn):
                # fileList = os.listdir()
                # with open('list', 'wb') as fp:
                # pickle.dump(fileList, fp)
                # f = open('list')
                # headerEncoder(f, conn)
                # files = os.listdir()
                # liststr = listtostring(files)
                # conn.send(b'HELP PLEASE......')
                # sendFile(f, conn)

                def retr(conn):
                    conn.send("continue".encode())
                    filename = conn.recv(1024).decode()
                    file = open(filename, "rb")
                    conn.sendall(file.read())

                def stor(conn):
                    conn.send("continue".encode())
                    filename = conn.recv(1024).decode()
                    chunk = conn.recv(4096)
                    with open(filename, 'wb+') as file:
                        file.write(chunk)

                while True:
                    try:
                        command = client.recv(1024).decode()
                        print("Command: " + str(command))
                        success = "operation completed!"
                        if not command:
                            break
                        print("Command received: (" + str(command) + ") from address: " + str(address))

                        if command == 'list':
                            list(client)
                            print("%s" % success)
                        elif command == 'retrieve':
                            retr(client)
                            print("%s" % success)
                        elif command == 'store':
                            stor(client)
                            print("%s" % success)
                    except:
                        print("CONNECTION TERMINATED: " + str(address))
                        client.close()
                        return False

            if __name__ == "__main__":
                while True:
                    port_num = input("type port to be used: \n")
                    try:
                        port_num = int(port_num)
                        break
                    except ValueError:
                        pass


        print("server now running on port %d." % port_num)
        Server('', port_num).listen()