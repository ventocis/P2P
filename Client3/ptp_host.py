import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ftp_client import *
from ftp_server import *
import os
import threading

name = None
connSocket = None
ftpSocket = None

class Server(threading.Thread):
    def __init__(self, port):
        self.port = port
        super(Server, self).__init__()
    def run(self):
        beginConn(self.port)

def connectToServer():
    global connSocket
    global name
    global server_field
    global port_field
    global name_field
    global hostname_field
    global tkvar

    server = server_field.get()
    name = name_field.get()
    port = port_field.get()
    hostName = hostname_field.get()
    connSpeed = tkvar.get()

    if server == "" or port == "" or name == "" or hostName == "":
        messagebox.showerror("Error", "Please fill all fields")
        return
    conn = connect(server, port, name, hostName, connSpeed)
    if conn != 505:
        serverPort = int(conn[1])
        connSocket = conn[0]
        fileDesc("filelist.xml", name, connSocket)
        serverSide = Server(serverPort)
        serverSide.start()
    else:
    	messagebox.showerror("Error", "Could not connect to server...")

def searchFiles():
    global name
    global connSocket
    global sr
    global keyword_field

    srchString = keyword_field.get()
    if name == None or connSocket == None:
        messagebox.showerror("Error", "Have not connected to server...")
        return
    search(srchString, name, connSocket)
    results = None
    with open('key_search.txt', 'r') as f:
        results = f.readlines()
    sr.delete(*sr.get_children())
    for r in results:
        info = r.split()
        p = str(int(info[1]))
        sr.insert("", "end", values = (info[3], info[0] + ":" + p, info[2]))
    os.remove("key_search.txt")

def disconnectServer():
    global name
    global connSocket

    quitServer(name, connSocket)
    connSocket = None
    messagebox.showinfo("Disconnected", "You have disconnected from the centralized server.")

def ftp():
    global command_field
    global commands
    global ftpSocket
    command = command_field.get()
    tokens = command.split()
    commands.insert("end", ">>" + command + "\n")
    if tokens[0] == "CONNECT":
        if len(tokens) != 3:
            commands.insert("end", "INCORRECT NUMBER OF ARGUMENTS\n")
            return
        if ftpSocket != None:
            commands.insert("end", "PLEASE USE QUIT BEFORE CONNECTING TO ANOTHER HOST\n")
        ftpSocket = ftp_connect(tokens[1], int(tokens[2]))
        if ftpSocket == 505:
            commands.insert("end", "ERROR CONNECTING\n")
            ftpSocket = None
            return
        else:
            commands.insert("end", "SUCCESSFULLY CONNECTED TO " + tokens[1] + ":" + tokens[2] + "\n")
        
    if tokens[0] != "CONNECT":
        if ftpSocket == None:
            commands.insert("end", "PLEASE CONNECT BEFORE USING ANOTHER COMMAND\n")
        if tokens[0] == "RETR" and len(tokens) == 2:
            retr(command, ftpSocket)
        elif tokens[0] == "QUIT" and len(tokens) == 1:
            quit(ftpSocket)
            commands.insert("end", "YOU'VE ENDED THE FTP SESSION\n")
        else:
            commands.insert("end", "INVALID COMMAND, TRY AGAIN\n")
root = tk.Tk()
root.title("GV-NAPSTER Host")

connect_frame = tk.Frame(root)
connect_frame.pack()

tk.Label(connect_frame, text = "Server Hostname").grid(row = 0, column = 0)
tk.Label(connect_frame, text = "Port").grid(row = 0, column = 2)
tk.Label(connect_frame, text = "Username").grid(row = 1, column = 0)
tk.Label(connect_frame, text = "Hostname").grid(row = 1, column = 2)
tk.Label(connect_frame, text = "Speed").grid(row = 1, column = 4)

server_field = tk.Entry(connect_frame)
port_field = tk.Entry(connect_frame)
name_field = tk.Entry(connect_frame)
hostname_field = tk.Entry(connect_frame)

server_field.grid(row = 0, column = 1)
port_field.grid(row = 0, column = 3)
name_field.grid(row = 1, column = 1)
hostname_field.grid(row = 1, column = 3)

tkvar = tk.StringVar(root)
options = {"Ethernet", "T1", "T3"}
tkvar.set("Ethernet")
speeds = tk.OptionMenu(connect_frame, tkvar, *options)
speeds.config(width = 20)
speeds.grid(row = 1, column = 5)

# insert command argument when able
connect_button = tk.Button(connect_frame, text = "Connect", command = connectToServer)
connect_button.grid(row = 0, column = 4)


search_frame = tk.Frame(root)
search_frame.pack()

search_top = tk.Frame(search_frame)
search_bottom = tk.Frame(search_frame)
search_top.pack(side = tk.TOP)
search_bottom.pack(side = tk.BOTTOM)

tk.Label(search_top, text = "Keyword").grid(row = 0, column = 0)

keyword_field = tk.Entry(search_top)
keyword_field.grid(row = 0, column = 1)

search_button = tk.Button(search_top, text = "Search", command = searchFiles)
search_button.grid(row = 0, column = 2)

#search results
sr = ttk.Treeview(search_bottom)
sr["columns"] = ("1", "2", "3")
sr.column("#0", stretch = tk.NO)
sr.column("1", stretch = tk.NO)
sr.column("2", stretch = tk.NO)
sr.column("3", stretch = tk.NO)

sr.heading("1", text = "Speed", anchor = tk.W)
sr.heading("2", text = "Hostname", anchor = tk.W)
sr.heading("3", text = "Filename", anchor = tk.W)

sr.grid(row = 1, column = 1)

ftp_frame = tk.Frame(root)
ftp_frame.pack(side = tk.BOTTOM)

ftp_top = tk.Frame(ftp_frame)
ftp_bottom = tk.Frame(ftp_frame)
ftp_top.grid(row = 0)
ftp_bottom.grid(row = 1)

tk.Label(ftp_top, text = "Enter Command").grid(row = 0, column = 0)
command_field = tk.Entry(ftp_top)
command_field.grid(row = 0, column = 1)
go_button = tk.Button(ftp_top, text = "Go", command = ftp)
go_button.grid(row = 0, column = 2)

scroll = tk.Scrollbar(ftp_bottom)
scroll.pack(side = tk.RIGHT, fill=tk.Y)

commands = tk.Text(ftp_bottom, height = 10, yscrollcommand = scroll.set)
scroll['command'] = commands.yview

disconnect = tk.Button(ftp_bottom, text = "Disconnect", command = disconnectServer)
disconnect.pack(side = tk.BOTTOM)
commands.pack(side = tk.LEFT)
root.mainloop()
