import socket
import threading
import pickle
from db_handler import Db_Handler
import log_handler
import request_model

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
        data = receive_data(conn)
        # data = conn.recv(1024)
        print("Received",pickle.loads(data)[0].operation)
        parsed_data = pickle.loads(data)
        print(parsed_data)
        res = True
        for request in parsed_data:
            if request.operation == "create":
                res = res and db_handler.create_user(request.person_data.name, request.person_data.last_name, request.person_data.email, request.person_data.phone)
            elif request.operation == "fetch" and len(parsed_data) == 1:
                res = res and db_handler.fetch_users()
        print("Respuesta",res)
        conn.sendall(pickle.dumps(res))


db = Db_Handler()
log = log_handler.Log_H()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5001))
server.listen(1)
while True:
    conn, addr = server.accept()
    threading.Thread(target=request_handler, args=(conn, db, log), daemon=True).start()
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
