import threading

# import library of socket
import socket

import os
import sqlite3
import protocols as protocl

Create_User = 'INSERT OR IGNORE INTO User(username, password, online) VALUES (?,?,?)'
Get_Users = 'SELECT * FROM User WHERE username = ?'
Set_Off = 'UPDATE SET online = 1 WHERE username = ?'
Get_Id = 'SELECT id FROM User WHERE username = ?'

def check_users(user):
    with sqlite3.connect('database.sqlite3') as connection:
        users = connection.cursor()
        users.execute(Get_Users,(user,))
        return users.fetchall()

def get_id(user):
    with sqlite3.connect('database.sqlite3') as connection:
        users = connection.cursor()
        users.execute(Get_Id, (user,))
        data = users.fetchall()
        return data[0][0]

def set_online(user):
    with sqlite3.connect('database.sqlite3') as connection:
        connection.execute(Set_Off,user)
        return connection.commit()

def set_offline(user):
    with sqlite3.connect('database.sqlite3') as connection:
        connection.execute(Set_Off, user)
        return connection.commit()

#print(check_users(username))

def register_validation(username, password):
    if len(check_users(username)) == 0:
        if len(password) > 5:
            register(username,password)
            return ("success")
        else:
            return ("passLimited")
    else:
        return ("duplicate")

def register(user_name,pass_word):
    with sqlite3.connect('database.sqlite3') as connection:
        connection.execute(Create_User, tuple((user_name, pass_word,1)))
        connection.commit()

########################################################################

IP = '127.0.0.1'
PORT = '100002'

class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):

        # AF_INET for IPV4
        # define protocl TCP (STREAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(3)
        print("Listening at", sock.getsockname())

        while True:

            # Accepting new connection
            sc, sockname = sock.accept()
            print(f"Accepting a new connection from {sc.getpeername()} to {sc.getsockname()}")

            # Create a new thread
            server_socket = ServerSocket(sc, sockname, self)

            # start new thread
            server_socket.start()

            # Add thread to active connection
            self.connections.append(server_socket)
            print("Ready to recieve messages from", sc.getpeername())

    def broadcast(self, message, source):
        for connection in self.connections:
           # send to all connected client accept the source client
           if connection.sockname != source:
               connection.send(message)

    def remove_connection(self, connection):
        self.connections.remove(connection)

class ServerSocket(threading.Thread):

    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server


    def run(self):
        flag = False
        while True:
            message = self.sc.recv(1024).decode('UTF-8')
            if message:
                if flag == True:
                    print(f"{message}")
                    #msg = protocl.client_register(user_name)
                    # self.sc.send(msg.encode())
                    self.sc.send(message.encode())
                    # self.server.broadcast(message, self.sockname)

                if message.find('Make') != -1:
                    # print(protocl.split_client_register(message))
                    username, password = protocl.split_client_register(message).split("--")
                    tempString = register_validation(username, password)
                    if tempString == 'success':
                        register(username, password)
                        print(f"{message}")
                        print(protocl.accepted_client_register(get_id(username)))
                        flag = True
                        self.sc.send(tempString.encode())
                        self.server.broadcast(tempString, self.sockname)
                    else:
                        self.sc.send(tempString.encode())
                        self.server.broadcast(tempString, self.sockname)


                if message == "exit":
                    set_offline(username)

            else:
                print(f"{self.sockname} has closed the connection")
                server.remove_connection(self)

    def send(self, message):

        self.sc.sendall(message.encode('UTF-8'))

def _exit(server):

    while True:
        ipt = input("")
        if ipt == "q":
            print("Closing all connection...")
            for connection in server.connections:
                connection.sc.close()

            print("Shutting down he server")
            os._exit(0)


if __name__ == '__main__':
    server = Server('127.0.0.1', 50000)
    server.start()
    finish = threading.Thread(target=exit, args=(server,))
    finish.start()