import socket
from threading import Thread
import sqlite3


def registration(client):
    connection = sqlite3.connect("Unlucky.db")
    cursor = connection.cursor()

    nickname = client.recv(BUFSIZ).decode("utf8")
    password = client.recv(BUFSIZ).decode("utf8")

    mySQLQuery = ("""
                        INSERT INTO Users(Nickname, Password)
                        VALUES('{}','{}')

                            """).format(nickname, password)
    cursor.execute(mySQLQuery)
    connection.commit()
    connection.close()
    print(nickname + " has been registered by Admin.")


def authentication(client):
    connection = sqlite3.connect("Unlucky.db")
    cursor = connection.cursor()

    while True:
        nickname = client.recv(BUFSIZ).decode("utf8")
        password = client.recv(BUFSIZ).decode("utf8")

        mySQLQuery = ("""
                           SELECT Nickname, Password
                           FROM Users
                           WHERE Nickname = '{}' AND Password = '{}'
                       """).format(nickname, password)

        cursor.execute(mySQLQuery)
        results = cursor.fetchall()
        if len(results) != 0:
            client.send(bytes("Accepted", "utf8"))
            connection.close()
            return nickname
        else:
            client.send(bytes("Declined", "utf8"))


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        try:
            client, client_address = SERVER.accept()
            name = authentication(client)
            print("%s:%s has connected." % client_address)
            addresses[client] = client_address
            Thread(target=handle_client, args=(client, name)).start()
        except OSError:
            print("Authentication error: %s:%s" % client_address)


def handle_client(client, name):
    """Handles a single client connection."""
    welcome = 'Welcome to the chat, %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("b233e775d63bb8b86cf031776d4caea613f59cda", "utf8"):
                registration(client)

            elif msg != bytes("{quit}", "utf8"):
                broadcast(msg, name + ": ")

            else:
                print("%s:%s has disconnected." % addresses[client])
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                break
        except OSError:
            client.close()
            del clients[client]
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1488
print("Address: " + HOST)
print("Port: " + str(PORT))
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Server started!")
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
