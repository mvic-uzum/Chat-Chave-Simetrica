#! /usr/bin/env python

import socket
import sys
import time
import threading
import select
import traceback
from cryptography.fernet import Fernet

#key simétrica gerada uma vez aleatoriamente e mantida fixa
key = 'mCEMtu9N5Bc8L0IP11I3V5S6EbSftia5OjrY42DR_pY='
fernet = Fernet(key)

class Server(threading.Thread):
    def initialise(self, receive):
        self.receive = receive

    def run(self):
        lis = []
        lis.append(self.receive)
        while 1:
            read, write, err = select.select(lis, [], [])
            for item in read:
                try:
                    s = item.recv(1024)
                    if s != '':
                        chunk = s
                        print(fernet.decrypt(chunk).decode() + '\n>>') #Decriptagrafa a mensagem e a exibe
                except:
                    traceback.print_exc(file=sys.stdout)
                    break


class Client(threading.Thread):
    def connect(self, host, port):
        self.sock.connect((host, port))

    def client(self, host, port, msg):
        sent = self.sock.send(msg)
        # print "Sent\n"

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            host = input("Enter the server IP \n>>")
            port = int(input("Enter the server Destination Port\n>>"))
        except EOFError:
            print("Error")
            return 1

        print("Connecting\n")
        s = ''
        self.connect(host, port)
        print("Connected\n")
        user_name = input("Enter the User Name to be Used\n>>")
        receive = self.sock
        time.sleep(1)
        srv = Server()
        srv.initialise(receive)
        srv.daemon = True
        print("Starting service")
        srv.start()
        while 1:
            msg = input('>>')
            if msg == 'exit':
                break
            if msg == '':
                continue
            msg = user_name + ': ' + msg
            data = fernet.encrypt(msg.encode())
            self.client(host, port, data)
        return (1)

if __name__ == '__main__':
    print("Starting client")
    cli = Client()
    cli.start()
