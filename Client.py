import socket
import win32file
import win32con
import win32com
import sys
import os

from Server import Server


BUFFER_SIZE = 2048
IP = "127.0.0.1"
PORT = 12345
DIRECTORY_PATH=r"C:\Users\USER\Downloads"
FILE_LIST_DIRECTORY = 0x0001

class Client:
    def __init__(self, IP:str = IP, PORT:int = 12345, directory_path:str=DIRECTORY_PATH) -> None:
        self.client_socket = socket.socket()
        self.directory_path = directory_path
        print(self.read_directoty_changes())
        self.client_socket.connect((IP,PORT))
    
    def send_file(self, file_name:str = "Books.exe"):
        file = open(file_name,"r")
        
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
        return win32file.ReadDirectoryChangesW(hDir,BUFFER_SIZE,False,win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,None,None)

if __name__ == "__main__":
    main = Client(IP,PORT,DIRECTORY_PATH)