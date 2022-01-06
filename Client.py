import socket
import win32file
import win32con
import win32com
import sys
import os
import threading

BUFFER_SIZE = 2048
IP = "127.0.0.1"
PORT = 12345
DIRECTORY_PATH="C:\\Users\\USER\\Downloads\\"
FILE_LIST_DIRECTORY = 0x0001
LOGFILE = "answers.txt"
class Client:
    def __init__(self, IP:str = IP, PORT:int = PORT, directory_path:str=DIRECTORY_PATH) -> None:
        self.directory_path = directory_path
        self.files_list = []
        self.client_socket = socket.socket()
        self.client_socket.connect((IP,PORT))

    # CHECK
    def send_file(self):
        while True:
            if self.files_list:
                file = open(DIRECTORY_PATH + self.files_list[0],"rb")
                content = file.read()
                file.seek(0)
                packets = len(content)//BUFFER_SIZE + 1
                self.client_socket.send(str(packets).encode())
                if self.client_socket.recv(2) == "ok".encode():
                    for i in range(packets):
                        self.client_socket.send(file.read(BUFFER_SIZE))
                    analysis = self.client_socket.recv(BUFFER_SIZE)
                    with open(LOGFILE, "a") as logfile:
                        logfile.write(f"{self.files_list[0]}: {analysis.decode()}\n")
                    self.files_list.pop(0)
                else:
                    sys.stderr("didn't get an answer from the server")

    # FIN
    def read_directoty_changes(self) -> str:
        hDir = win32file.CreateFile (
            self.directory_path,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
        while True:
            change = win32file.ReadDirectoryChangesW(hDir,BUFFER_SIZE,False,win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,None,None)[0]
            print(change)
            self.files_list.append(change[1])

    def main(self):
        directory_check = threading.Thread(target=self.read_directoty_changes)
        client_send = threading.Thread(target=self.send_file)
        directory_check.start()
        client_send.start()
if __name__ == "__main__":
    main = Client(IP,PORT,DIRECTORY_PATH)
    main.main()