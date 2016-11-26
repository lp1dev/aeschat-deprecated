from modules.aescipher import AESCipher
from modules.utils import error
from getpass import getpass
import json

class KeyStore(object):
    def __init__(self, filename):
        self.filename = filename
        self.aes = None
        
    def build(self, password=None):
        passes = []
        if self.aes is None:
            if password is None:
                password = getpass("KeyStore password : ")
            self.aes = AESCipher(password.replace("\n", ""))
        with open(self.filename, "wb") as f:
            f.write(self.aes.encrypt(json.dumps(passes)))
            
    def get_passes(self, password=None):
        if self.aes is None:
            if password is None:
                password = getpass("KeyStore password : ")
            self.aes = AESCipher(password.replace("\n", ""))
        with open(self.filename, "r") as f:
            try:
                return json.loads(self.aes.decrypt(f.read()))
            except ValueError:
                error("Password is invalid or keystore file is corrupted")
                return None        

    def add_password(self, nick, ip, newpass=None, password=None):
        if self.aes is None:
            if password is None:
                password = getpass("KeyStore password : ")
            self.aes = AESCipher(password.replace("\n", ""))
        passes = self.get_passes(password)
        if newpass is None:
            newpass = getpass("Password for user %s :" %nick).replace("\n", "")
        for index, entry in enumerate(passes):
            if passes[index]['login'] == nick:
                passes[index]['password'] = newpass
                passes[index]['ip'] = ip
                with open(self.filename, "wb") as f:
                    f.write(self.aes.encrypt(json.dumps(passes)))
                return newpass
        passes.append({"login":nick, "password":newpass, "ip":ip})
        with open(self.filename, "wb") as f:
            f.write(self.aes.encrypt(json.dumps(passes)))
        return newpass

    def get_password(self, login):
        if self.aes is None:
            password = getpass("KeyStore password : ")
            self.aes = AESCipher(password.replace("\n", ""))
        passes = self.get_passes()
        if passes is not None:
            for password in passes:
                if password['login'] == login:
                    return password['password']
        return None
