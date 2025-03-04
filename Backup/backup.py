import socket
from db_handler import Db_Handler
from connection_backup import Connection
import pickle

def write_to_file(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            print('Received:', data.decode())
            f = open("file.txt", "at")
            f.write(data.decode()+" ")
            f.close()
        except ConnectionRefusedError:
            break


def request_handler(db_handler,parsed_data):
    print(parsed_data)
    res = None
    if parsed_data.operation == "create":
        res = db_handler.create_user(parsed_data.person_data.name, parsed_data.person_data.last_name, parsed_data.person_data.email, parsed_data.person_data.phone)
    elif parsed_data.operation == "fetch":
        res = db_handler.fetch_users()
    print("Respuesta",res)
    return res

def handle_response(conn, parsed_data, response):
    if parsed_data[0] == "create":
        res = 0
        for item in response:
            res = res or item
            conn.sendall(pickle.dumps(res))
    elif parsed_data[0] == "fetch":
        #logica de selección
        conn.sendall(pickle.dumps(response[0]))



def backup_handler(conn,backup,db_handler,data):
    parsed_data = pickle.loads(data)
    res_backup = request_handler(db_handler, parsed_data)
    response = [res_backup]
    if parsed_data.sender == "client":
        backup.send_data(backup.client, data)
        res1 = backup.receive_data(backup.client, DECODE=True)
        response.append(res1)
        print("respuesta del pc1", res1)

        backup.send_data(backup.client2, data)
        res2 = backup.receive_data(backup.client2, DECODE=True)
        response.append(res2)
        print("respuesta del pc2", res2)
        handle_response(conn,parsed_data,response)
    else:
        backup.send_data(conn, pickle.dumps(res_backup))


        
backup = Connection()
db = Db_Handler()
while True:
    conn, addr = backup.accept()
    print('Connected by', addr, conn.getsockname()[1])
    while True:
        data = backup.receive_data(conn)

        if not data:
            break
        backup_handler(conn,backup,db,data)




client.close()
client2.close()
conn.close()


