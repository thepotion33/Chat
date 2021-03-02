import hashlib
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import traceback
import tkinter
from tkinter import messagebox
import sys

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print('Error: ', text)
    messagebox.showerror(title="Error", message=text)
    quit()


sys.excepthook = log_uncaught_exceptions


def receive(event=None):
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def registration(event=None):

    def reg_button(event=None):
        nickname = nic_entry.get()
        password = pas_entry.get()
        hpas = hashlib.sha1(password.encode())
        htmp = hpas.hexdigest()
        client_socket.send(bytes(nickname, "utf8"))
        client_socket.send(bytes(htmp, "utf8"))
        knopka.place_forget()
        nic_entry.place_forget()
        pas_entry.place_forget()
        reglabel1.place_forget()
        reglabel2.place_forget()

        ###
        def reg_return(event=None):
            knopka.place_forget()
            lb.place_forget()
            bt.place_forget()
            entry_field.place(x=10, y=400, width=300)
            send_button_iz.place(x=320, y=400)
            registration_button.place(x=360, y=400, width=130)
        ###

        lb = tkinter.Label(top, text="User has been registered!", fg="green", font=("Ubuntu", 10), bg="#3c3f41")
        bt = tkinter.Button(top, text="OK")
        bt.bind("<Button-1>", reg_return)

        lb.place(x=10, y=400, width=420)
        bt.place(x=463, y=400)

    client_socket.send(bytes("b233e775d63bb8b86cf031776d4caea613f59cda", "utf8"))

    registration_button.place_forget()
    entry_field.place_forget()
    send_button_iz.place_forget()

    Nickname.set("")
    Password.set("")

    nic_entry = tkinter.Entry(top, textvariable=Nickname, font=("Ubuntu", 10))
    pas_entry = tkinter.Entry(top, textvariable=Password, font=("Ubuntu", 10))
    reglabel1 = tkinter.Label(top, text="Nickname:", font=("Ubuntu", 10), bg="#3c3f41", fg="#dbedff")
    reglabel2 = tkinter.Label(top, text="Password:", font=("Ubuntu", 10), bg="#3c3f41", fg="#dbedff")
    knopka = tkinter.Button(top, text="Send", font=("Ubuntu", 10))
    knopka.bind("<Button-1>", reg_button)

    knopka.place(x=449, y=400)
    nic_entry.place(x=80, y=400)
    pas_entry.place(x=299, y=400)
    reglabel1.place(x=10, y=400)
    reglabel2.place(x=230, y=400)


def authentication(event=None):
    nickname = entry1.get()
    password = entry2.get()
    hpas = hashlib.sha1(password.encode())
    htmp = hpas.hexdigest()
    client_socket.send(bytes(nickname, "utf8"))
    client_socket.send(bytes(htmp, "utf8"))
    msg = client_socket.recv(BUFSIZ).decode("utf8")
    if msg == "Accepted":
        global checkadm

        if nickname == "Admin":
            checkadm = True
        else:
            checkadm = False

        button.place_forget()

        lb = tkinter.Label(au, text="Nickname and Password are correct!", fg="green", font=("Ubuntu", 10), bg="#3c3f41")
        lb.place(x=20, y=80, width=230)
        bt = tkinter.Button(au, text="OK", font=("Ubuntu", 10), bg="#c8312b", fg="#dbedff")
        bt.bind("<Button-1>", au_destroy)
        bt.place(x=331, y=80)

    else:
        lb2 = tkinter.Label(au, text="Nickname and Password are incorrect!", fg="red", font=("Ubuntu", 10), bg="#3c3f41")
        lb2.place(x=20, y=80)
        button.place(x=320, y=80)


def au_destroy(event=None):
    au.quit()
    au.destroy()


def send(event=None):
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()


def get_address(event=None):
    global HOST
    global PORT
    HOST = host.get()
    PORT = port.get()
    if not HOST:
        messagebox.showwarning("Warning", "You must enter the values!")
        return
    if not PORT.isdigit():
        messagebox.showwarning("Warning", "Host variable must be an integer!")
    else:
        connect.destroy()


# Sockets
connect = tkinter.Tk()
connect.title("Connection")
connect.geometry('340x130')
connect.configure(background="#2a2e33")
connect.resizable(width=False, height=False)
HOST, PORT = "", ""
host, port = tkinter.StringVar(), tkinter.StringVar()

label1 = tkinter.Label(connect, text="Host:", font=("Ubuntu", 10), bg="#3c3f41", fg="#dbedff")
label2 = tkinter.Label(connect, text="Port:", font=("Ubuntu", 10), bg="#3c3f41", fg="#dbedff")
entry1 = tkinter.Entry(connect, textvariable=host, bg="#45494a", fg="#dbedff", font=("Ubuntu", 12))
entry1.focus()
entry2 = tkinter.Entry(connect, textvariable=port, bg="#45494a", fg="#dbedff", font=("Ubuntu", 12))
button = tkinter.Button(connect, text="Send", font=("Ubuntu", 10), bg="#c8312b", fg="#dbedff")
button.bind("<Button-1>", get_address)
button.bind("<Return>", get_address)

label1.place(x=20, y=20)
label2.place(x=22, y=50)
entry1.place(x=60, y=20, width=270)
entry2.place(x=60, y=50, width=270)
button.place(x=175, y=80)

connect.mainloop()

# Port management

if not PORT:
    PORT = 1488
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
# Authentication

au = tkinter.Tk()
au.title("Authentication")
au.geometry('370x130')
au.resizable(width=False, height=False)
au.configure(background="#2a2e33")

Password, Nickname = tkinter.StringVar(), tkinter.StringVar()

label1 = tkinter.Label(au, text="Nickname:", font=("Ubuntu", 10), bg="#3c3f41", fg="#dbedff")
label2 = tkinter.Label(au, text="Password:", font=("Ubuntu", 10), bg="#3c3f41", fg="#dbedff")
entry1 = tkinter.Entry(au, textvariable=Nickname, bg="#45494a", fg="#dbedff", font=("Ubuntu", 12))
entry2 = tkinter.Entry(au, textvariable=Password, show="•", bg="#45494a", fg="#dbedff", font=("Ubuntu", 12))
button = tkinter.Button(au, text="Send", font=("Ubuntu", 10), bg="#c8312b", fg="#dbedff")
button.bind("<Button-1>", authentication)
button.bind("<Return>", authentication)

label1.place(x=20, y=20)
label2.place(x=20, y=50)
entry1.place(x=91, y=20, width=270)
entry2.place(x=91, y=50, width=270)
button.place(x=190, y=80)

au.protocol("WM_DELETE_WINDOW", sys.exit)
au.mainloop()

# Chat
if checkadm:
    top = tkinter.Tk()
    top.title("Televiber")
    top.geometry('500x440')
    top.resizable(width=False, height=False)
    top.configure(background="#2a2e33")
    my_msg = tkinter.StringVar()
    my_msg.set("")

    messages_frame = tkinter.Frame(top)
    scrollbar = tkinter.Scrollbar(messages_frame)
    msg_list = tkinter.Listbox(messages_frame, height=45, width=100, yscrollcommand=scrollbar.set)
    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    send_button_iz = tkinter.Button(top, text="Send", command=send)
    registration_button = tkinter.Button(top, text="Register")
    registration_button.bind("<Button-1>", registration)

    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    messages_frame.place(x=10, y=10, width=480, height=380)
    entry_field.place(x=10, y=400, width=300)
    send_button_iz.place(x=320, y=400)
    registration_button.place(x=360, y=400, width=130)

    top.protocol("WM_DELETE_WINDOW", on_closing)
else:
    top = tkinter.Tk()
    top.title("Televiber")
    top.geometry('500x440')
    top.resizable(width=False, height=False)
    top.configure(background="#3c3f41")
    my_msg = tkinter.StringVar()
    my_msg.set("")

    messages_frame = tkinter.Frame(top)
    scrollbar = tkinter.Scrollbar(messages_frame)
    msg_list = tkinter.Listbox(messages_frame, height=45, width=100, yscrollcommand=scrollbar.set)
    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    send_button_iz = tkinter.Button(top, text="Send", command=send)
    send_button_iz.bind("<Button-1>", send)

    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    messages_frame.place(x=10, y=10, width=480, height=380)
    entry_field.place(x=10, y=400, width=300)
    send_button_iz.place(x=320, y=400, width=170)

    top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive)
receive_thread.start()
top.mainloop()
