import socket
import os
import pickle
import threading

class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print("New connection from: " + str(address))
            client.settimeout(60)
            threading.Thread(target=self.ClientListener, args=(client, address)).start()
    def ClientListener(self, client, address):
        def ListToString(s):
            str = ""
            for element in s:
                str += " " + element
            return str

        def list_sender(conn):
            files = os.listdir()
            liststr = ListToString(files)
            # send data to the client
            print(liststr)

        while True:
            try:
                command = client.recv(1024).decode()
                print("Command recieved: " + str(command))
                success = "operation completed!"
                if not command:
                    print(command + "is the command")
                    break
                if str(command) == 'list':
                    print("made it to list command list")
                    list_sender(client)
                    print("%s" % success)

                elif command == 'retrieve':
                    filename = client.recv(1024).decode()
                    # open the file stream
                    file = open(filename, "rb")
                    # send the file
                    client.sendall(file.read())
                elif command == 'store':
                    filename = client.recv(1024).decode()
                    print(filename)
                    chunk = client.recv(4096)
                    with open(filename, 'wb+') as file:
                        file.write(chunk)
                else:
                    print("Received nothing")
            except:
                print("Connection closed from: " + str(address))
                client.close()
                return False

if __name__ == "__main__":
    while True:
        port_num = input("Enter Port Number -> ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    print("The server is now running on port %d." % port_num)
    Server('', port_num).listen()
