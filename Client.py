""" The program is a client that looks for changes
    and new files in the "Downloads" directory then
    sends them to the server (that checks them) recievs
    the server's report on the file and prints it to the
    log file. 
"""
import socket
import win32file
import win32con
import sys
import threading
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
    logging.basicConfig(filename=CONSTS["client"]["logfile"],
                format='%(asctime)s %(message)s',
                filemode='w')


class Client:
    def __init__(self, ip: str, port: int, directory_path: str) -> None:
        """ The constructor initializes the directory path and the files list
            and connects to the server via the ip and port given.

            :param ip: The ip address of the server.
            :type ip: str
            :param port: The port of the server.
            :type port: int
            :param directory_path: The path to the directory you want to secure
            :type directory_path: str  
        """
        self.directory_path = directory_path
        self.files_list = []
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.client_socket = socket.socket()
        self.logger.info("Connecting to the server")
        self.client_socket.connect((ip, port))
        self.logger.info("connection established")
        self.main()

    def read_directoty_changes(self) -> None:
        """ The function checks for updates in the wanted directory with winapy.
            If there is a new file in the directory the function
            uppends it to the files_list member.
        """
        # Creating a handle for the directory.
        hDir = win32file.CreateFile(
            self.directory_path,
            0x0001,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
        while True:
            # Reading changes in the directory.
            self.logger.info("waiting for directory changes")
            change = win32file.ReadDirectoryChangesW(
                hDir, CONSTS["client"]["buffer_size"], False, win32con.FILE_NOTIFY_CHANGE_LAST_WRITE, None, None)[0]
            self.files_list.append(change[1])
            self.logger.info("added a directory change")

    def send_file(self) -> None:
        """ The function checks for updates in the files_list for new files to send to the server.
            When it finds a new file it sends it to the server.
        """
        while True:
            if self.files_list:
                self.logger.info("reading a new file")
                file = open(self.directory_path + self.files_list[0], "rb")
                content = file.read()
                file.seek(0)
                packets = len(content)//CONSTS["server"]["buffer_size"] + 1
                self.logger.info("sending packets amount")
                self.client_socket.send(str(packets).encode())
                self.logger.info("receiving ok")
                if self.client_socket.recv(2) == "ok".encode():
                    self.logger.info("sending the file")
                    for i in range(packets):
                        self.client_socket.send(
                            file.read(CONSTS["server"]["buffer_size"]))
                    self.logger.info("receiving report")
                    analysis = self.client_socket.recv(
                        CONSTS["client"]["buffer_size"])
                    self.logger.info("writing report")
                    with open(CONSTS["client"]["files_logfile"], "a") as logfile:
                        logfile.write(
                            f"{self.files_list[0]}: {analysis.decode()}\n")
                    self.files_list.pop(0)
                else:
                    self.logger.error("didn't get an answer from the server")

    def main(self) -> None:
        """ The function sets off the whole client class via threads.
        """
        directory_check = threading.Thread(target=self.read_directoty_changes)
        client_send = threading.Thread(target=self.send_file)
        directory_check.start()
        client_send.start()


if __name__ == "__main__":
    config()
    main = Client(CONSTS["client"]["ip"], CONSTS["client"]
                  ["port"], CONSTS["client"]["directory_path"])
