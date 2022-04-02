import threading
import socket
import os
import sys
import tkinter as tk
import protocols as protocol

global user

def header():
    print("Welcome to Chatroom App\r\n" +
          "This app Written by Mostafa Fazli for Network lesson of Shahroud university of technology\r\n" +
          "************************************************\r\n")



class Send(threading.Thread):

    # Listens for user input from command line
    # sock the connected sock object
    # name (str) : The username provided by the user

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        # Listen for user input from the command line and send it  ti the
        # Typing "Quit will close the connection and exit the app

        while True:
            print('{}: '.format(self.name), end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            # if we type "QUIT"  we leave the chatroom
            if message == "QUIT":
                self.sock.sendall('Server: {} has left the chat'.format(self.name).encode('UTF-8'))
                msg = "exit"
                self.sock.send(msg.encode())
                break

            # send message to server for breadcasting
            else:
                self.sock.sendall('{}: {}'.format(self.name , message).encode('UTF-8'))

        print('\nQuitting')
        msg = "exit"
        self.sock.send(msg.encode())
        self.sock.close()
        os._exit(0)

class Recieve(threading.Thread):

    # Listens for incoming messages from the server
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.message = None

    def run(self):

        # Recieve data from the server and displays it in the gui
        while True:
            message = self.sock.recv(1024).decode('UTF-8')

            if message:
                if self.message:
                    self.messages.insert(tk.END, message)
                    print('hi')
                    print('\r{}\n{}: '.format(message, self.name), end='')
                else:
                    print('\r{}\n{}: '.format(message, self.name), end='')

            else:
                print('\n No. We have lost connection to the server!')
                print('\nQuitting...')
                self.sock.close()
                os._exit(0)

class Client:

    # Management of client-server connection and integration of GUI
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.password = None
        self.messages = None

    def get_username_register(self):
        username = input("Write your username\r\n")
        global user
        user = username
        return username

    def get_password_register(self):
        password = input("Write your password\r\n")
        return password

    def signup(self):
        user_name = self.get_username_register()
        user_password = self.get_password_register()
        return protocol.client_register(user_name, user_password)

    def get_command(self):
        print("What do you want ? \r\n" +
              "1. Register\r\n" +
              "2. Login \r\n")
        command = input("Select an option:\r\n")

        if command == '1':
            print("Register Mode")
            return self.signup()

        elif command == '2':
            print("Login Mode")

        else:
            print("Wrong command, try again !!!")


    def start(self):

        header()

        print('Trying to connect to {}:{}...'.format(self.host, self.port))

        self.sock.connect((self.host, self.port))

        print('Seccessfully connected to {}:{}'.format(self.host, self.port))

        print()

        msg =  self.get_command()
        self.sock.send(msg.encode())
        tempString = self.sock.recv(1024).decode('UTF-8')
        if(tempString == 'success'):
            self.name = user
            print('Welcome, {}! Getting ready to send and receive messages...'.format(self.name))

            # Create send and recieve threads
            send = Send(self.sock, self.name)
            receive = Recieve(self.sock, self.name)

            # start send and receive thread
            send.start()
            receive.start()
            self.sock.sendall('server: {} joined the chat\r\n'.format(self.name).encode())
            print("\rReady! Leave te chatroom anytime by typing QUIT\n")
            print(f"you said: ")
            return receive

        elif tempString == 'passLimited':
            print("Your password should be at lease 6 character\r\n")
            self.sock.close()

        elif tempString == 'duplicate':
            print("There is another account with this username\r\n"
                  "If this is your username, log in to your account from the login section\r\n"
                  "Otherwise select a specific username\r\n")
            self.sock.close()



    def send(self, textInput):

        # Sends textInput data frm the GUI
        message = textInput.get()
        textInput.delete(0, tk.END)
        self.messages.insert(tk.END)

        # Type "QUIT" to leave the chatroom
        if message == "QUIT":
            self.sock.sendall('Server: {} has left the chat.'.format(self.name).encode('UTF-8'))

            print('\nQuitting...')
            self.sock.close()
            os._exit(0)

        # SEND message to the server for broadcasting
        else:
            self.sock.sendall('{}: {}'.format(self.name, message).encode('UTF-8'))

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
    client = Client('127.0.0.1', 50000)
    receive = client.start()
