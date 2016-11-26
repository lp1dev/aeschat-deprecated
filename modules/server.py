from socket import socket, AF_INET, SOCK_STREAM
from modules.aesqueue import Queue
from modules.client import Client
from modules.utils import notify, message
from modules.connections import Connection
from modules.keystore import KeyStore
from modules.utils import debug, error
from conf import debugmode, login, keystore_file
from modules.aescipher import AESCipher
from os.path import isfile
from sys import stdin
import binascii

class Server(object):
    def __init__(self, address, recv_size=2048):
        self.address = address
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.bind(self.address)
        self.socket.listen(5)
        self.inputs = [self.socket , stdin]
        self.outputs = []
        self.message_queue = Queue
        self.recv_size = recv_size
        self.encoding = "utf-8"
        self.connections = []

    def handle_writable(self, writable):
        return self.inputs, self.outputs

    def user_input(self, input):
        if input[0] == '/':
            c = Client()
            return c.execute(input, self)
        return False

    def handle_hello(self, socket, content, autor, peername):
        c = Connection(socket, peername[0], self.address[1])
        c.login = autor
        c.password = self.keystore.get_password(autor)
        if c.password is None:
            c.password = self.keystore.add_password(autor)
        c.aes = AESCipher(c.password)
        c.peername = peername
        self.connections.append(c)
        if socket not in self.outputs:
            self.outputs.append(socket)
        return False

    def handle_message(self, socket, content, autor, peername, raw_message, length):
        for index, connection in enumerate(self.connections):
            if connection.socket == socket:
                try:
                    if connection.aes is not None:
                        content = content[:int(length)]
                        content = connection.aes.decrypt(content)
                except binascii.Error as e:
                    if debugmode:
                        print(e)
                    error("Password seems invalid for user %s" %autor)
        message("[%s] : %s" %(autor, content))
        return False

    def close_socket(self, socket):
        if socket in self.outputs:
            self.outputs.remove(socket)
        if socket in self.inputs:
            self.inputs.remove(socket)
        socket.close()

    def handle_incoming_message(self, raw_message, peername, socket):
        if debugmode:
            debug("Incoming message : %s" %raw_message)
        message = str(raw_message, self.encoding).replace("\n", "")
        message = message.split("|;")
        if len(message) != 4:
            print("Received malformed message : %s" %message)
            self.close_socket(socket)
        else:
            header, autor, length ,content = message
            if header == "hello":
                notify("%s connected" %autor)
                self.handle_hello(socket, content, autor, peername)
            if header == "message":
                self.handle_message(socket, content, autor, peername, raw_message, length)

    def disconnect_client(self, socket):
        for index, connection in enumerate(self.connections):
            if connection.socket == socket:
                if connection.login is not None:
                    notify("client %s disconnected" %connection.login)
                else:
                    notify("client %s disconnected" %connection.socket)
                self.close_socket(connection.socket)
                self.connections.pop(index)

    def handle_readable(self, readable):
        for socket in readable:
            if socket is self.socket:
                connection, client_address = socket.accept()
                connection.setblocking(0)
                if debugmode:
                    print("Connection : %s" %connection)
                connection.send(("%s" %login).encode(self.encoding))
                self.inputs.append(connection)
                return False
            elif socket is stdin:
                return self.user_input(socket.readline().replace("\n", ""))
            else:
                try:
                    data = socket.recv(self.recv_size)
                    if data:
                        self.handle_incoming_message(data, socket.getpeername(), socket)
                        return False
                    else:
                        self.disconnect_client(socket)
                except ConnectionResetError as e:
                    print(e)
                    self.disconnect_client(socket)
                    return False
            return False
        return False
