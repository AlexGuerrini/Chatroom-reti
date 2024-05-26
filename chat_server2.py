#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def accetta_connessioni_in_entrata():
    while True:
        try:
            client, client_address = SERVER.accept()
            logging.info(f"Connessione da {client_address}")
            print("%s:%s si è collegato." % client_address)
            client.send(bytes("Digita il tuo nome e premi invio", "utf8"))
            indirizzi[client] = client_address
            Thread(target=gestice_client, args=(client,)).start()
        except Exception as e:
            logging.error(f"Errore durante l'accettazione di una connessione: {e}")

def gestice_client(client):
    try:
        nome = client.recv(BUFSIZ).decode("utf8")
        benvenuto = f'Benvenuto {nome}! Puoi scrivere {{quit}} per uscire.'
        client.send(bytes(benvenuto, "utf8"))
        msg = f"{nome} si è unito alla chat!"
        broadcast(bytes(msg, "utf8"))
        clients[client] = nome
        broadcast_user_list()

        while True:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):
                client.send(bytes("{quit}", "utf8"))
                time.sleep(0.5)  # Aggiungi un ritardo per garantire che i messaggi siano inviati
                client.close()
                del clients[client]
                broadcast(bytes(f"{nome} ha abbandonato la Chat.", "utf8"))
                broadcast_user_list()
                break
            else:
                broadcast(msg, nome + ": ")
    except ConnectionResetError:
        logging.info(f"Il client {clients[client]} ha chiuso la connessione.")
        if client in clients:
            nome = clients[client]
            del clients[client]
            broadcast(bytes(f"{nome} ha abbandonato la Chat.", "utf8"))
            broadcast_user_list()
    except Exception as e:
        logging.error(f"Errore nella gestione del client {client}: {e}")
        if client in clients:
            del clients[client]

def broadcast(msg, prefisso=""):
    for utente in clients:
        try:
            utente.send(bytes(prefisso, "utf8") + msg)
        except Exception as e:
            logging.error(f"Errore durante l'invio del messaggio a {utente}: {e}")

def broadcast_user_list():
    user_list_msg = "Utenti connessi:\n" + lista_utenti()
    for utente in clients:
        try:
            utente.send(bytes(user_list_msg, "utf8"))
        except Exception as e:
            logging.error(f"Errore durante l'invio della lista utenti a {utente}: {e}")

def lista_utenti():
    utenti = [nome for client, nome in clients.items()]
    return "\n".join(utenti)

clients = {}
indirizzi = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    logging.info("Server in attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()