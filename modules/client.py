from modules.connections import Connection
from modules.utils import warning
from modules.aescipher import AESCipher
from conf import secret, debugmode, login
import socket

class Client(object):
    def exit(self, input, server):
        server.socket.close()
        return True
    
    def connect(self, input, server):
        port = 9000
        command = input.split(" ")
        if len(command) > 1:
            ip = input.split(" ")[1]
            if ":" in ip and len(ip.split(":")) == 2:
                ip , port = ip.split(":" )
            print("Connecting to.. %s:%s" %(ip, port))
            server.connections.append(Connection(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ip, port))
            server.connections[len(server.connections) - 1].begin()
            server.connections[len(server.connections) - 1].log_user(server)
            if server.connections[len(server.connections) - 1].socket not in server.inputs:
                server.inputs.append(server.connections[len(server.connections) - 1].socket)
        return False

    def send(self, input, server):
        command = input.replace("/send ", "").split(" ")
        if len(command) > 1:
            print(command)
            recipient = command[0]
            message = command[1]
            message = input.replace(recipient, "").replace("/send", "")
            raw_message = message[2:]
            encrypted_message = self.aes.encrypt(raw_message)
            for index, connection in enumerate(server.connections):
                if connection.login is not None and connection.login.replace(" ", "") == recipient.replace(" ", ""):
                    message = ("%s|;%s|;%s|;" %("message", login, len(encrypted_message))).encode(server.encoding)
                    connection.socket.send(message + encrypted_message)
                    return False
            warning("%s there is no such user" %recipient)
            return False
        warning("%s malformed command" %input)
        return False

    def help(self, input, server):
        print("\n/help    \tshow this prompt\n/connect\tip[:port]\n/send    \tlogin message")
        return False
    
    def __init__(self):
        self.commands = {
            "/connect" : self.connect,
            "/exit" : self.exit,
            "/send" : self.send,
            "/help" : self.help
        }
        self.sock = None
        self.connections = []
        self.aes = AESCipher(secret)
        
    def execute(self, input, server):
        for command in self.commands.keys():
            if command in input:
                return self.commands[command](input, server)
        print("Unknown command")
        return False
