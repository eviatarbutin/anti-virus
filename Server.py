import socket
import sys
import os

BUFFER_SIZE = 2048

class Server:
    def __init__(self, IP:str = "0.0.0.0", PORT:int = 12345) -> None:
        self.server_socket = socket.socket()
        self.server_socket.bind((IP,PORT))
        self.server_socket.listen(1)
        self.client_socket, self.client_address = self.server_socket.accept()
    
    def get_file(self):
        content = self.client_socket.recv(BUFFER_SIZE)

        #recive the file
        file = open("temp_file","wb+")
        file.write(content)
        file.close()