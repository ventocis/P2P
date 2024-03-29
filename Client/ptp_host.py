import tkinter as tk
from tkinter import ttk
from ftp_client import *

# def search(keyword):

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
connect_button = tk.Button(connect_frame, text = "Connect")
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

search_button = tk.Button(search_top, text = "Search")
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

#dummy results
sr.insert("", 'end', values = ("T1", "121.121.12.1", "yup.txt"))
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
go_button = tk.Button(ftp_top, text = "Go")
go_button.grid(row = 0, column = 2)

scroll = tk.Scrollbar(ftp_bottom)
scroll.pack(side = tk.RIGHT, fill=tk.Y)

commands = tk.Text(ftp_bottom, height = 10, yscrollcommand = scroll.set)
scroll['command'] = commands.yview
commands.pack(side = tk.LEFT)
root.mainloop()
