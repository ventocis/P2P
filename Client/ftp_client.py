import socket
import sys
import socketserver
from os import listdir, path
from os.path import isfile, join
import os

PORT = 12000

class FileListener(socketserver.BaseRequestHandler):

    def search(self, command):
        self.request.send("searchh".encode('utf-8'))
        stringFromServ = self.request.recv(1024).decode('utf-8')
        with open('key_search.txt', 'w') as f:
            while stringFromServ != "EOF SEARCH":
                f.write(stringFromServ + "\n")
                stringFromServ = None
                self.request.send("Next String".encode('utf-8'))
                stringFromServ = self.request.recv(1024).decode('utf-8')

    def fileDesc(self, command):        
        fileName = command[2].strip()
        with open(fileName, 'r') as fs:
            for line in fs:
                self.request.send(line.encode('utf-8'))
            self.request.close()
            print("File Uploaded")
        

    def handle(self):
        print("Handling...")
        recvStr = self.request.recv(1024).decode('utf-8')
        command = recvStr.split()
        if command[0] == "ACK" and command[1] == "FILEDESC":
            self.fileDesc(command)
        elif command[0] == "ACK" and command[1] == "SEARCH":
            self.search(command)
        else:
            print("Skipped it")
        return 

def createPort(command):
    global PORT
    PORT = PORT + 2
    print(str(PORT))

    # Create a socket to handle the data connection
    serv = socketserver.TCPServer(('127.0.0.1', PORT), FileListener)
    print(serv)
    serv.handle_request()

#Creates the data socket on a new port, sends the port the data socket is on over the command connection
#& then waits for the reply from the server on the data socket
def setupSocket(command, sock):
    global PORT
    # Change the port so that we open the data socket on a new port
    command = command + " " + str(PORT + 2)
    print(str(command))
    #send a message to say that we have opened the data connection socket & include the port number
    sock.send(str(command).encode('utf-8'))

    serv = None
    try:
        print("creating port")
        createPort(command)
    except:
        print("error creating port")
    print(sock)
     #wait for the reply from the server on the data socket

#Sends the search command to the server
def search(srchString, userName, sock):
    print("In search")
    command = "SEARCH " + srchString + " " + userName
    setupSocket(command, sock)

#Sends "FILEDESC fileName userName" to the server if the file exists
def fileDesc(fileName, userName, sock):
    command = "FILEDESC " + fileName + " " + userName
    if os.path.exists(fileName):
        print("File " + fileName + " found")
        setupSocket(command, sock)
    else:
        print("File Not Found")

#Sends "QUIT username" to the server & closes the server
def quitServer(userName, sock):
    command = "QUIT " + userName
    sock.send(command.encode('utf-8'))
    print("CLOSING CONNECTION TO SERVER...GOODBYE")
    sock.close()

def quit(sock):
    command = "QUIT"
    sock.send(command.encode('utf-8'))
    sock.close()

#Establishes the initial control connection
def connect(server, port, userName, hostName, connSpeed):
    print("in connect")
    intPort = int(port)
    if intPort != 12000:
        print("INCORRECT PORT")
        return 505
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server,intPort))
        command = "CONNECT " + userName + " " + hostName + " " + connSpeed
        print("setting up socket...")
        setupSocket(command, sock)
        print("Connected to " + server)
        return sock
    except:
        print("ERROR: Invalid IP or port")
        return 505

