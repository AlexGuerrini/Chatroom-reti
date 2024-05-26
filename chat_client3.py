#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg.startswith("Utenti connessi:"):
                user_list.delete(0, tkt.END)
                for user in msg.split('\n')[1:]:
                    user_list.insert(tkt.END, user)
            else:
                msg_list.insert(tkt.END, msg)
                msg_list.see(tkt.END)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        finestra.quit()

def on_closing(event=None):
    my_msg.set("{quit}")
    send()

finestra = tkt.Tk()
finestra.title("CHATROOM")

# Creazione dei frame
left_frame = tkt.Frame(finestra, bg="lightgrey")
right_frame = tkt.Frame(finestra)

# Lista utenti
user_list_label = tkt.Label(left_frame, text="Utenti Connessi", bg="lightgrey")
user_list_label.pack(padx=10, pady=5)
user_list = tkt.Listbox(left_frame, height=20, width=25, bg="white")
user_list.pack(padx=10, pady=5)

# Frame dei messaggi
messages_frame = tkt.Frame(right_frame)
my_msg = tkt.StringVar()
my_msg.set("Scrivi qui i tuoi messaggi.")
scrollbar = tkt.Scrollbar(messages_frame)

# Lista dei messaggi
msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set, bg="white")
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH, padx=5, pady=5)
msg_list.pack()
messages_frame.pack(pady=5)

# Campo di input
entry_field = tkt.Entry(right_frame, textvariable=my_msg, width=50)
entry_field.bind("<Return>", send)
entry_field.pack(pady=5)
send_button = tkt.Button(right_frame, text="Invia", command=send)
send_button.pack()

# Posizionamento dei frame
left_frame.pack(side=tkt.LEFT, fill=tkt.Y, padx=10, pady=10)
right_frame.pack(side=tkt.RIGHT, fill=tkt.BOTH, expand=True, padx=10, pady=10)

finestra.protocol("WM_DELETE_WINDOW", on_closing)

# Connessione al Server
HOST = input('Inserire il Server host: ')
PORT = input('Inserire la porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkt.mainloop()