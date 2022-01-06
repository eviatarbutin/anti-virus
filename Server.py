""" The program is a server that gets files from the client
    checks them via virustotal and returns the information 
    about this file. 
"""

import socket
import vt
import base64
import json
import logging

CONSTS: dict = {}


def config(config_file_name: str = "config.json"):
    """ The fucnction sets constants according to the json config file.
        :param config_file_name: The filename of the config file.
        :type config_file_name: str
    """
    global CONSTS
    with open(config_file_name, "r") as config_file:
        CONSTS = json.load(config_file)


class Server:
    def __init__(self, ip: str, port: int) -> None:
        """ The functions takes the server parameters(ip and port)
            listens and accept one client.

            :param ip: The ip address where the server shall be bound.
            :type ip: str
            :param port: The port where the server shall be bound.
            :type port: int
        """
        self.server_socket = socket.socket()
        self.server_socket.bind((ip, port))
        self.server_socket.listen(1)
        self.client_socket, self.client_address = self.server_socket.accept()

        self.main()

    def get_file(self) -> bytes:
        """ The function recieves the length of the file
            and then the file itself from the client and
            returns it's contents.

            :returns: the contents of a file.
            :rtype: bytes 
        """
        # Receive the number of packets that the client will send the file within.
        packets = int(self.client_socket.recv(10).decode())
        self.client_socket.send("ok".encode())  # send ok response
        file: bytes = self.client_socket.recv(CONSTS["client"]["buffer_size"])
        for i in range(packets-1):
            # receive the whole file
            file += self.client_socket.recv(CONSTS["client"]["buffer_size"])
        return file

    def check_file(self, file_contents: bytes) -> str:
        """ The function  takes the file contents save them
            as a file and sends them to virustotal for a check
            then return the report from virustotal

            :param file_contents: the contents of a file 
                that was sent from the client for a check.
            :type file_contents: bytes
            :returns: the report from virustotal
            :rtype: str
        """
        # Save the file.
        with open("temp_file.bin", "wb") as temp_file:
            temp_file.write(file_contents)
        client = vt.Client(CONSTS["server"]["api_key"])
        temp_file = open("temp_file.bin", "rb")
        # Let virustotal analise the file.
        # You can change this to true but the analise might take some time then.
        analysis = str(client.scan_file(temp_file, False)).split()[1] 
        temp_file.close()
        ob = client.get_object("/files/" + base64.b64decode(analysis).decode()
                               [:base64.b64decode(analysis).decode().find(":")])
        client.close()
        return str(ob.last_analysis_stats)

    def send_response(self, report: str) -> None:
        """ The function takes the report about the file from the
            check_file function and sends it back to the client


            :param report: The report about the file which is sent to the client.
            :type report: str
        """
        self.client_socket.send(report.encode())

    def main(self):
        """The function sets off the whole server."""
        while True:
            self.send_response(self.check_file(self.get_file()))


if __name__ == "__main__":
    config()
    main = Server(CONSTS["server"]["ip"], CONSTS["server"]["port"])
