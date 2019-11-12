import socket
import sys
import socketserver
from os import listdir, path
from os.path import isfile, join
import os

PORT = 12000
sock = None
serv = None


class FileListener(socketserver.BaseRequestHandler):
    # def retr(self, command):
    #     print("called this 2")
    #     if command[1] == "200":
    #         #myPath = '/Users/samventocilla/Code/cis457DataComm/Proj1/CIS457Proj1/Client/'
    #         fileName = command[2]
    #         fileName = fileName.strip()
    #         f = open(fileName, "w")
    #         self.request.send(("200").encode('utf-8'))
    #         print("Created file " + fileName)
    #         line = self.request.recv(1024).decode('utf-8')
    #         while line:
    #             f.write(line)
    #             self.request.send(("200").encode('utf-8'))
    #             line = self.request.recv(1024).decode('utf-8')
    #         f.close()
    #         print("File Downloaded")
    #     elif command[1] == "550":
    #         print("File not found")

    def search(self, command):
        self.request.send("searchh".encode('utf-8'))
        stringFromServ = self.request.recv(1024).decode('utf-8')

        while stringFromServ != "EOF SEARCH":
            print(stringFromServ)
            stringFromServ = None
            self.request.send("Next String".encode('utf-8'))
            stringFromServ = self.request.recv(1024).decode('utf-8')
        

    def stor(self, command):
        fileName = command[1].strip()
        with open(fileName, 'r') as fs:
            for line in fs:
                self.request.send(line.encode('utf-8'))
            self.request.close()
            print("File Uploaded")


    def list(self, command):
        if len(command) <= 1:
            print("No files to list")
        else:
            print("Files stored:")
            for x in command:
                if x != "LIST":
                    print("\t" + x)

    def fileDesc(self, command):        
        fileName = command[2].strip()
        with open(fileName, 'r') as fs:
            for line in fs:
                self.request.send(line.encode('utf-8'))
            self.request.close()
            print("File Uploaded")
        

    def handle(self):
        print("In handle")    
        recvStr = self.request.recv(1024).decode('utf-8')
        print(recvStr)
        command = recvStr.split()
        print("Command "+ str(command))
        if command[0] == "ACK" and command[1] == "FILEDESC":
            self.fileDesc(command)
        elif command[0] == "ACK" and command[1] == "SEARCH":
            self.search(command)
        elif command[0] == "STOR":
            print("stor")
        if command[0] == "RETR":
            self.retr(command)
        elif command[0] == "LIST":
            self.list(command)
        else:
            print("Skipped it")
        return 

ip = None
port = None

#Creates the data socket on a new port, sends the port the data socket is on over the command connection
#& then waits for the reply from the server on the data socket
def setupSocket(command):
    global PORT
    global serv
    # Change the port so that we open the data socket on a new port
    PORT = PORT + 2
    command = command + " " + str(PORT)

    # Create a socket to handle the data connection
    serv = socketserver.TCPServer(('127.0.0.1', PORT), FileListener)

    #send a message to say that we have opened the data connection socket & include the port number
    sock.send(command.encode('utf-8'))
    print("got here1")

    #wait for the reply from the server on the data socket
    serv.handle_request()
    print("got here")

#Sends the search command to the server
def search(srchString, userName):
    print("In search")
    command = "SEARCH " + srchString + " " + userName
    setupSocket(command)

#Sends "FILEDESC fileName userName" to the server if the file exists
def fileDesc(fileName, userName):
    command = "FILEDESC " + fileName + " " + userName
    if os.path.exists(fileName):
        print("File " + fileName + " found")
        setupSocket(command)
    else:
        print("File Not Found")

#Sends "QUIT username" to the server & closes the server
def quit(userName):
    command = "QUIT " + userName
    sock.send(command.encode('utf-8'))
    print("CLOSING CONNECTION TO SERVER...GOODBYE")
    sys.exit()

#Establishes the initial control connection
def connect(server, port, userName, hostName, connSpeed):
    global sock
    global serv
    print("in connect")
    intPort = int(port)
    if intPort != 12000:
        print("INCORRECT PORT")
        return
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server,intPort))
        print("Connected to " + server)
        command = "CONNECT " + userName + " " + hostName + " " + connSpeed
        setupSocket(command)
    except:
        print("ERROR: Invalid IP or port")
        return 505

