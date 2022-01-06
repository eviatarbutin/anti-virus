import socket
import sys
import os
import vt
import base64

BUFFER_SIZE = 2048
API_KEY = "bc182bc090a7fcbfbd55eed1cc8d4636f5ebf5546e19bf7243836dc06575695d"

class Server:
    def __init__(self, IP: str = "0.0.0.0", PORT: int = 12345) -> None:
        self.server_socket = socket.socket()
        self.server_socket.bind((IP,PORT))
        self.server_socket.listen(1)
        self.client_socket, self.client_address = self.server_socket.accept()


    def get_file(self) -> bytes:
        packets = int(self.client_socket.recv(10).decode())
        self.client_socket.send("ok".encode())
        file:bytes = self.client_socket.recv(BUFFER_SIZE)
        for i in range(packets-1):
            file += self.client_socket.recv(BUFFER_SIZE)
        return file

    def check_file(self, file_contents: bytes) ->str:
        client = vt.Client(API_KEY)
        with open("temp_file.bin","wb") as temp_file:
            temp_file.write(file_contents)
        temp_file =  open("temp_file.bin","rb")
        print("scanning")
        analysis = str(client.scan_file(temp_file, True)).split()[1]
        temp_file.close()
        ob = client.get_object("/files/" + base64.b64decode(analysis).decode()[:base64.b64decode(analysis).decode().find(":")])
        print(ob.last_analysis_stats)
        client.close()
        return ob.last_analysis_stats

    def send_response(self, response):
        self.client_socket.send(str(response).encode())

    def main(self):
        while True:
            self.send_response(self.check_file(self.get_file()))

if __name__ == "__main__":
    main = Server()
    main.main()
    
    