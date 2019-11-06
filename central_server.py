import socket
import threading
import os
import xml.etree.ElementTree as ET


IP = '127.0.0.1'
PORT = 12000

class Client(threading.Thread):
    def __init__(self, s, addr):
        self.request = s
        self.addr = addr
        super(Client, self).__init__()

    def run(self):
        while(True):
            #wait for client to send username, hostname, and connection speed
            #store username, hostname, and connection speed in a table/list
            #send acknowledgement back to client
            #wait for client to send xml file with shared file descriptions
            #parse xml file and store descriptions in a table/list
            #wait for user to send a keyword search

    def stor(self, s, fileName):
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

    def parseXML(self, fileName, userName):
        if path.exists(fileName):
            tree = ET.parse(fileName)
            root = tree.getroot()
            for child in root:
                name = child[0]
                descr = child[1]
                #call function to store files
            print("Successfully parsed XML file")
        else:
            print("Parse Failed")
            s.send("Parse Failed".encode('utf-8'))
        os.remove(fileName)

    def quit(self):
        print("Client Has Disconnected")
        self.request.close()    

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((IP, PORT))
serv.listen(1)

while True:
    conn, addr = serv.accept()
    print("USER: " + str(addr) + " CONNECTED")
    client_thr = Client(conn, addr)
    client_thr.start()