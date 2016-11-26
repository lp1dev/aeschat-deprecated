from modules.utils import notify
from modules.aescipher import AESCipher
from conf import login, encoding
from getpass import getpass

class Connection(object):
    def __init__(self, socket, host, port):
        self.host = host
        self.port = port
        self.server = False
        self.logged = False
        self.socket = socket
        self.login = None
        self.password = None
        self.encoding = "utf-8"
        self.aes = None

    def begin(self):
        self.socket.connect((self.host, int(self.port)))
        
    def log_user(self, server):
        self.socket.send(str.encode("hello|;%s|;checksum|;hello" %login))
        self.login = self.socket.recv(server.recv_size).decode(encoding)
        self.password = server.keystore.get_password(self.login.replace(" ", ""))
        if self.password is None:
            self.password = getpass("Password for user %s : " %self.login)
        self.aes = AESCipher(self.password)
        notify("Successfully connected widh %s" %self.login)
        self.server = True
