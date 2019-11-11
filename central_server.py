import socket
import threading
import os
import xml.etree.ElementTree as ET
from os import listdir, path


IP = '127.0.0.1'
PORT = 12000
userDict = {}
fileList = []

class Client(threading.Thread):
    def __init__(self, s, addr):
        self.request = s
        self.addr = addr
        self.port = addr[1]
        super(Client, self).__init__()

    def run(self):
        while (True):
            print("received command")
            command = self.request.recv(1024).decode('utf-8').split()
            print(command)
            if command[0] == "CONNECT":
                print("Called connect")
                self.connect(command)
                return
                    
            #CONNECT Username Hostname ConnectionSpeed
            #Send ACK command name
            #FILEDESC FileName Username
            #SEARCH DESCR Username
            #LOCATION list
            #QUIT Username
            #wait for client to send username, hostname, and connection speed
            #store username, hostname, and connection speed in a table/list
            #send acknowledgement back to client
            #wait for client to send xml file with shared file descriptions
            #parse xml file and store descriptions in a table/list
            #wait for user to send a keyword search
    def connect(self, command):
        try:
            port = int(command[4])
            self.storeUsers(command[1], command[2], port, command[3])
            while(True):
                command = self.request.recv(1024).decode('utf-8').split()
                if command[0] == "QUIT":
                    self.quit(command[1])
                    return
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((IP, port))
                if command[0] == "FILEDESC":
                    print("got filedesc")
                    s.send("ACK FILEDESC".encode('utf-8'))
                    print("afteer ack")
                    self.stor(s, command[1])
                    self.parseXML(s, command[1], command[2])
                elif command[0] == "SEARCH":
                    self.search(command[1], command[2], s)
        except socket.error as exc:
            print("Connection error: " + str(exc))

    def stor(self, s, fileName):
        print("in stor")
        myString = "STOR "
        myString = myString + fileName
        s.send(myString.encode('utf-8'))
        f = open(fileName, "w")
        print("Created file " + fileName)
        line = s.recv(1024).decode('utf-8')
        while line:
            f.write(line)
            line = s.recv(1024).decode('utf-8')
        f.close()
        print("File Downloaded")

    def parseXML(self, s, fileName, userName):
        if path.exists(fileName):
            tree = ET.parse(fileName)
            root = tree.getroot()
            for child in root:
                name = child[0].text
                descr = child[1].text
                self.storeFiles(userName, name, descr)
            print("Successfully parsed XML file")
            os.remove(fileName)
        else:
            print("Parse Failed")
            s.send("Parse Failed".encode('utf-8'))

    def quit(self, userName):
        self.deleteUser(userName)
        print("Client Has Disconnected")
        self.request.close()

    def storeUsers(self, username, hostName, portNumber, connSpeed):
        userInfo = [hostName, portNumber, connSpeed]
        userDict[username] = userInfo

    def storeFiles(self, userName, fileName, description):
        fileInfo = [userName, fileName, description]
        fileList.append(fileInfo)
        
    def deleteUser(self, username):
        for file in fileList:
            if file[0] == username:
                fileList.remove(file)
        userDict.pop(username, None)

    def search(self, srchString, userName, s):
        #Let the client know that we are running the search so that it knows what to branch to
        s.send("SEARCH".encode('utf-8'))
        for file in fileList:
            if srchString in file[1] or srchString in file[2]:
                user = userDict[file[0]]
                rtrnString = user[0] + " " + user[1] + " " + file[2] + " " + user[2]    #hostname port fileName connSpeed
                s.send(rtrnString.encode('utf-8'))
        s.send("ACK SEARCH".encode('utf-8'))
        
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))
serv.listen(1)

while True:
    conn, addr = serv.accept()
    print("USER: " + str(addr) + " CONNECTED")
    client_thr = Client(conn, addr)
    client_thr.start()