import socket
import sys
import socketserver
from os import listdir, path
from os.path import isfile, join
import os

PORT = 12000
COUNT = 1

class FileListener(socketserver.BaseRequestHandler):
    def retr(self, command):
        print("called this 2")
        if command[1] == "200":
            #myPath = '/Users/samventocilla/Code/cis457DataComm/Proj1/CIS457Proj1/Client/'
            fileName = command[2]
            fileName = fileName.strip()
            f = open(fileName, "w")
            self.request.send(("200").encode('utf-8'))
            print("Created file " + fileName)
            line = self.request.recv(1024).decode('utf-8')
            while line:
                f.write(line)
                self.request.send(("200").encode('utf-8'))
                line = self.request.recv(1024).decode('utf-8')
            f.close()
            print("File Downloaded")
        elif command[1] == "550":
            print("File not found")

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

    def handle(self):
        print("In handle")    
        recvStr = self.request.recv(1024).decode('utf-8')
        command = recvStr.split()
        if command[0] == "RETR":
            self.retr(command)
        elif command[0] == "SEARCH":
            self.stor(command)
        elif command[0] == "LIST":
            self.list(command)
        else:
            print("Skipped it")
        return 

ip = None
port = None
 

def setupSocket(command):
    global PORT
    global COUNT
    global serv
    PORT = PORT + 2 * COUNT
    command = command + " " + str(PORT)
    serv = socketserver.TCPServer(('127.0.0.1', PORT), FileListener)
    print(sock)
    sock.send(command.encode('utf-8'))
    serv.handle_request()

def sendCommand(command):
    sock.send(command.encode('utf-8'))
    serv.handle_request()

def search(srchString, userName):
    print("In search")
    command = "SEARCH " + srchString + " " + userName
    sendCommand(command)

def fileDesc(fileName, userName):
    print("In fileDesc")
    command = "FILEDESC " + fileName + " " + userName
    if os.path.exists(fileName):
        print("File " + fileName + " found")
        sendCommand(command)
    else:
        print("File Not Found")

def quit(userName):
    command = "QUIT " + userName
    sock.send(command.encode('utf-8'))
    print("CLOSING CONNECTION TO SERVER...GOODBYE")
    sys.exit()

def connect(server, port, userName, hostName, connSpeed):
    global sock
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

