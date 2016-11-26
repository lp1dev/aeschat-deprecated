#!/usr/bin/python3

from select import select
from sys import exit, argv
from socket import socket, AF_INET, SOCK_STREAM
from modules.server import Server
from modules.aescipher import AESCipher
from modules.utils import notify
from modules.keystore import KeyStore
from modules.gfx import Gfx
from conf import gfx
from time import sleep
import threading

server_address = ("0.0.0.0", 9000)
if len(argv) == 3:
    server_address = (argv[1], int(argv[2]))
serv = Server(server_address)

def handle_sockets(readable, writable, exceptional, serv):
    stop = serv.handle_readable(readable)
    serv.handle_writable(writable)
    return stop, serv.inputs, serv.outputs

def start_server():
    stop = False
    notify("AESchat Server Running on port %s:%i" %(server_address))
    while stop is not True:
        readable, writable, exceptional = select(serv.inputs, serv.outputs, serv.inputs)
        stop, serv.inputs, serv.outputs = handle_sockets(readable, writable, exceptional, serv)
    print("\nGoodbye")
    serv.socket.close()
    return 0

def main():
    if gfx:
        serv.gfx = Gfx()
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()
    if gfx:
        serv.gfx.start()
    return 0

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("\nGoodbye")
        serv.socket.close()
