import socket
import sys
import os
import math

HOST = 0  # The server's hostname or IP address
PORT = 0  # The port used by the server

def client():

    the_socket = socket.socket()


    # this method is intended to recieve a list of files in the directory the server is currently in
    def list_receiver():
        the_socket.send(b'list')
        print("waiting to recieve")
        data = the_socket.recv(1024).decode()
        print(data)
        print("")

    #
    def retrieve(filename):
        the_socket.send(b'retrieve')
        # the_socket.recv(1024).decode()
        the_socket.send(filename.encode())
        dataChunk = the_socket.recv(4096)
        with open(filename, 'wb+') as f:
            f.write(dataChunk)


        print(filename + " received")

    def store(filename):
        the_socket.send(b'store')
        file = open(filename, "rb")
        the_socket.send(filename.encode())
        the_socket.sendall(file.read())
        print("File sent. ")

    def quitTransaction():
        the_socket.send(b'Reached quitTransaction()')
        the_socket.send(b'quit')
        the_socket.close()

    menu = 1
    connected = 0
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
            connector(the_socket, response[1], int(response[2]))
            connected = 1
        elif response[0] == "LIST" and connected == 1:
            list_receiver()
        elif response[0] == "RETRIEVE" and connected == 1:
            retrieve(response[1])
        elif response[0] == "STORE" and connected == 1:
            store(response[1])
        elif response[0] == "QUIT":
            menu = 0
            quitTransaction()
        elif connected == 0:
            print("Server and Client are not connected! You must connect to the server first!")
        else:
            print("NOT A VALID COMMAND! ")

    #print('Received', repr(data))
    print("connect")
    return the_socket


def connector(the_socket, IP, socketPort):
    global HOST
    global PORT
    HOST = IP
    PORT = socketPort
    the_socket.connect((HOST, PORT))
    the_socket.send(b'Connection Works')


client()


