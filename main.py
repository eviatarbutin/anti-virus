"""The program initiates the project (the server and the client)."""
from multiprocessing import Process
import time
import os
from subprocess import Popen
import sys


def run_client():
    if __name__ == "__main__":
        os.system("python3 Client.py")

def run_server():
    if __name__ == "__main__":
        os.system("python3 Server.py")



if __name__ == "__main__":
    server = Popen([sys.executable, "Server.py"])
    time.sleep(3)
    client = Popen([sys.executable, "Client.py"])
    client.wait()

    """
    server = Process(target=run_server)
    client = Process(target=run_client)

    server.run()
    time.sleep(5)
    client.run()
    """