import socket
import pickle

PC1_IP = '127.0.0.1'
PC1_PORT = 5001
PC2_IP = "127.0.0.1"
PC2_PORT = 5002
BACKUP_IP = '127.0.0.1'
BACKUP_PORT = 5010
SERVER_PORT = 5000

class Connection:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', SERVER_PORT))
        self.backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect()
        self.server.listen(1)

    def __del__(self):
        self.server.close()
        self.client.close()
        self.client2.close()
        self.backup.close()


    def _connect(self):
        self._connect_to_pc1()
        self._connect_to_pc2()
        self._connect_to_backup()
    
    def _connect_to_pc1(self):
        try:
            self.client.connect((PC1_IP, PC1_PORT))
        except:
            self.client.close()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Conexión fallida con pc1")
            
    def _connect_to_pc2(self):
        try:
            self.client2.connect((PC2_IP, PC2_PORT))
        except:
            self.client2.close()
            self.client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Conexión fallida con pc2")
            
    def _connect_to_backup(self):
        try:
            self.backup.connect((BACKUP_IP, BACKUP_PORT))
        except:
            self.backup.close()
            self.backup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Conexión fallida con backup")

    def _reconnect(self, conn):
        sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            if conn is self.client:
                sck.connect((PC1_IP, PC1_PORT))
                self.client = sck
            elif conn is self.client2:
                sck.connect((PC2_IP, PC2_PORT))
                self.client2 = sck
            elif conn is self.backup:
                sck.connect((BACKUP_IP, BACKUP_PORT))
                self.backup = sck
            conn.close()
            return True, sck
        except:
            return False, None

    
    def send_data(self, conn, data):
        try:
            conn.sendall(data)
        except:
            connection_status, new_conn = self._reconnect(conn)
            if connection_status:
                new_conn.sendall(data)
            else:
                return None
    
    def receive_data(self, conn, DECODE=False):
        BUFF_SIZE = 1024
        data = b''
        while True:
            try:
                part = conn.recv(BUFF_SIZE)
            except:
                break
            data+=part
            if len(part) < BUFF_SIZE:
                break
        if DECODE and data:
            return pickle.loads(data)
        elif data: 
            return data
        else:
            return 0

    def accept(self):
        return self.server.accept()