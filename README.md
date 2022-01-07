# anti-virus

In this project I've implemented a simple way to secure your Downloads directory with the virustotal API.         
The project works in a client-server model where the client is in charge of looking for directory changes andsending them to the server;
The server is in charge of saving the copy of the file and sending it for a scan to virustotal and then sending the report about the file to the client.

![external-content duckduckgo com](https://user-images.githubusercontent.com/58847763/148542532-76f77d82-db9f-400d-8848-56a3692661a1.jpg)


In this project I've used:        
- Winapi - to check for directory changes.          
- Threading - to allow the client multitask, send the file to the server and still being able to check for updates in the directory.
- Logging - for saving logs about server and client work.
- Json - to allow saving and easily changing project's configuration in a fixed place.
- subprocess - to allow running the program in much a easier way. 
- sockets - for server and client communication.
- virustotal api - to scan the files for viruses and other malicious contents.

## Instalation
Simply clone the project to the wanted directory on your computer and here you go.

## Usage
First of all you should change the config.json file according to your computer and wanted settings for example you most likely want to change the directory path according to the one on your machine.        
After the config.json is ready you can just run the main.py file by typing: "py main.py"/"python3 main.py"/"python main.py".       
Working with main.py is much easier but this feature is not fully checked so instead you can first run the Server.py and then the Client.py.
