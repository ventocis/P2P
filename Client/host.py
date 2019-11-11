import socket
import sys
import socketserver
import os
import ftp_client
import ftp_server

PORT = 12000
COUNT = 1

print("Welcome to our FTP Client!")
print("Commands")
print("CONNECT [ADDRESS] [PORT]: connects you to a server")
print("LIST: lists files on server")
print("RETR [FILENAME]: retrieves file on server")
print("STOR [FILENAME]: stores file on server")
print("QUIT: closes connection with server and exits the program")
print()

ip = None
port = None
sock = None
# Initial Connection to the concurrent server
while True:
    comm = input("INPUT COMMAND: ")
    tokens = comm.split()
    if tokens[0] == "CONNECT":
        if len(tokens) != 3:
            print("INCORRECT NUMBER OF ARGUMENTS")
            continue
        ip = tokens[1]
        port = int(tokens[2])
        if port != 12000:
            print("INCORRECT PORT")
            continue
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            print("Connected to " + ip)
        except:
            print("ERROR: Invalid IP or port")
            continue
        break
    else:
        print("MUST CONNECT BEFORE USING OTHER COMMANDS")
        continue

    #CONNECT Username Hostname ConnectionSpeed portNumber
    #Send ACK command name
    #FILEDESC FileName Username
    #SEARCH DESCR Username
    #LOCATION XMLFile
    #QUIT Username
    #ACK is ACK CONNECT
    #wait for client to send username, hostname, and connection speed
    #store username, hostname, and connection speed in a table/list
    #send acknowledgement back to client
    #wait for client to send xml file with shared file descriptions
    #parse xml file and store descriptions in a table/list
    #wait for user to send a keyword search

while True:
   comm = input("\nINPUT COMMAND: ")
   tokens = comm.split()
   if tokens[0] == "CONNECT" and len(tokens) == 4:
       ftp_client.retr(comm, sock)
   elif tokens[0] == "STOR" and len(tokens) == 2:
       ftp_client.stor(comm, sock)
   elif tokens[0] == "LIST" and len(tokens) == 1:
       ftp_client.listCMD(comm, sock)
   elif tokens[0] == "QUIT" and len(tokens) == 1:
       sock.send(comm.encode('utf-8'))
       print("CLOSING CONNECTION TO SERVER...GOODBYE")
       sys.exit()
   else:
       print("Invalid Command")


