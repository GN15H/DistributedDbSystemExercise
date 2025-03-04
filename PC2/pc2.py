import socket
import threading
import pickle
from db_handler import Db_Handler
import log_handler

def write_to_file(conn, addr):
    while True:
        data = conn.recv(1024)
        print('Received:', data.decode())
        f = open("file.txt", "at")
        f.write(data.decode()+" ")
        f.close()

def receive_data(conn, DECODE=False):
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

def request_handler(conn, db_handler, log):
    while True:
        data = conn.recv(1024)
        print("Received",pickle.loads(data).operation)
        parsed_data = pickle.loads(data)
        log.save_time(parsed_data.time)
        print(parsed_data)
        res = None
        if parsed_data.operation == "create":
            res = db_handler.create_user(parsed_data.person_data.name, parsed_data.person_data.last_name, parsed_data.person_data.email, parsed_data.person_data.phone)
        elif parsed_data.operation == "fetch":
            res = db_handler.fetch_users()
        print("Respuesta",res)
        conn.sendall(pickle.dumps(res))

log = log_handler.Log_H()
db = Db_Handler()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5002))
server.listen(1)
while True:
    conn, addr = server.accept()
    threading.Thread(target=request_handler, args=(conn, db,log), daemon=True).start()
    # print('Connected by', addr)
    # data = conn.recv(1024)
    # if data.decode() == "exit":
    #     print("Finalizando conexión")
        # break
    # print('Received:', data.decode())
    # f = open("file.txt", "at")
    # f.write(data.decode()+" ")
    # f.close()
conn.close()
