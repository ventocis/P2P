import socket
import sys
import socketserver
import os
import ftp_client
import ftp_server


# Initial Connection to the concurrent server


    #CONNECT Username Hostname ConnectionSpeed portNumber
    #Send ACK command name
    #FILEDESC FileName Username
    #SEARCH DESCR Username
    #LOCATION hostname port fileName connSpeed (repeats this for however many locations)
    #QUIT Username
    #ACK is ACK CONNECT
    #wait for client to send username, hostname, and connection speed
    #store username, hostname, and connection speed in a table/list
    #send acknowledgement back to client
    #wait for client to send xml file with shared file descriptions
    #parse xml file and store descriptions in a table/list
    #wait for user to send a keyword search


 #connect(servername, portnum, username, hostname, connspeed)
 #quit(username)
 #fileDesc(filename, username)
 #search(searchString, username)

print("Welcome to our FTP Client!")
print("Commands")
print("CONNECT [ADDRESS] [PORT]: connects you to a server")
print("LIST: lists files on server")
print("RETR [FILENAME]: retrieves file on server")
print("STOR [FILENAME]: stores file on server")
print("QUIT: closes connection with server and exits the program")
print()


while True:
    comm = input("\nINPUT COMMAND: ")
    tokens = comm.split()
    if tokens[0] == "CONNECT" and len(tokens) == 3:
        ftp_client.connect("127.0.0.1", 12000, "username", "hostname", "connspeed")
    elif tokens[0] == "FILEDESC" and len(tokens) == 3:
        ftp_client.fileDesc(tokens[1], tokens[2])
    elif tokens[0] == "SEARCH" and len(tokens) == 3:
        ftp_client.search(tokens[1], tokens[2])
    elif tokens[0] == "QUIT" and len(tokens) == 2:
        ftp_client.quit(tokens[1])
    else:
        print("Invalid Command")



