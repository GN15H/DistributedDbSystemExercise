import socket
import pickle

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
BACKUP_IP = '127.0.0.1'
BACKUP_PORT = 5010

class Connection:
    def __init__(self):
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._isServer = True
        self.connect_to_server()
    
    def connect_to_server(self):
        try:
            self.sck.connect((SERVER_IP, SERVER_PORT))
        except ConnectionRefusedError:
            try:
                self._isServer = False
                self.sck.connect((BACKUP_IP,BACKUP_PORT))
            except ConnectionRefusedError:
                print("Conexión no posible")
                quit()
            
    def reconnect_to_server(self):
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sck.connect((SERVER_IP,SERVER_PORT))
        except:
            return None
        self.sck.close()
        self.sck = sck
    
    def send_data(self, data):
        if not self._isServer:
            self.reconnect_to_server()
        try:
            self.sck.sendall(data)
        except ConnectionResetError:
            try:
                self.sck.close()
                sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sck.connect((BACKUP_IP,BACKUP_PORT))
                self.sck = sck
                self._isServer = False
                self.sck.sendall(data)
            except ConnectionRefusedError:
                print("Conexión no posible")
                quit()
    
    def receive_data(self):
        BUFF_SIZE = 1024
        data = b''
        while True:
            part = self.sck.recv(BUFF_SIZE)
            data+=part
            if len(part) < BUFF_SIZE:
                break
        return data
