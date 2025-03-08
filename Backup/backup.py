import socket
from db_handler import Db_Handler
from connection_backup import Connection
import pickle
import log_handler
import server_func
import storage_func

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
    res = True
    for request in parsed_data:
        if request.operation == "create":
            res = res and db_handler.create_user(request.person_data.name, request.person_data.last_name, request.person_data.email, request.person_data.phone)
        elif request.operation == "fetch":
            res = res and db_handler.fetch_users()
    print("Respuesta",res)
    return res

def handle_response(conn, parsed_data, response, log):
    if parsed_data[0].operation == "create":
        res = 0
        for item in response:
            res = res or item
        conn.sendall(pickle.dumps(res))
    elif parsed_data[0].operation == "fetch":
        #logica de selección
        max_index, max_timestamp = log.get_most_recent_updated()
        conn.sendall(pickle.dumps(response[0]))

def backup_handler(conn,backup,db_handler,data, log):
    parsed_data = pickle.loads(data)
    if not isinstance(parsed_data, list):
        parsed_data = [parsed_data]

    if len(parsed_data) == 1 and parsed_data[0].sender == "client" and parsed_data[0].operation != "update_log":
        return server_func.server_func(log=log, server=backup, conn=conn, data=data, db_handler=db_handler, parsed_data=parsed_data)
    elif len(parsed_data) == 1 and parsed_data[0].sender == "server" and parsed_data[0].operation == "update_log":
        conn.sendall(pickle.dumps(log.read_json()))
    else:
        log.update_json(parsed_data[0].log)
        return storage_func.request_handler_server(conn=conn, db_handler=db_handler, parsed_data=parsed_data, log=log)
    # res_backup = request_handler(db_handler, parsed_data)
    # response = [res_backup]
    # if len(parsed_data) == 1 and parsed_data[0].sender == "client":
    #     if parsed_data[0].operation == "create":
    #         conn.sendall(pickle.dumps("Servicio no disponible en este momento"))
    #         return None
    #     backup.send_data(backup.client, pickle.dumps(parsed_data))
    #     res1 = backup.receive_data(backup.client, DECODE=True)
    #     response.append(res1)
    #     print("respuesta del pc1", res1)

    #     backup.send_data(backup.client2, pickle.dumps(parsed_data))
    #     res2 = backup.receive_data(backup.client2, DECODE=True)
    #     response.append(res2)
    #     print("respuesta del pc2", res2)
    #     handle_response(conn,parsed_data,response, log)
    # else:
    #     backup.send_data(conn, pickle.dumps(res_backup))


        
backup = Connection()
db = Db_Handler()
log = log_handler.Log_H()
while True:
    conn, addr = backup.accept()
    print('Connected by', addr, conn.getsockname()[1])
    while True:
        data = backup.receive_data(conn)

        if not data:
            break
        backup_handler(conn,backup,db,data, log)


