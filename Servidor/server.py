import pickle
import log_handler
from connection_server import Connection
from request_model import Request_M
import sys

def handle_response(conn, data, response, log):
    parsed_data = pickle.loads(data)
    if parsed_data.operation == "create":
        res = 0
        for item in response:
            res = res or item
            conn.sendall(pickle.dumps(res))
    elif parsed_data.operation == "fetch":
        #logica de selección
        max_index, max_timestamp = log.get_most_recent_updated()
        conn.sendall(pickle.dumps(response[max_index]))



server = Connection()
log = log_handler.Log_H()
while True:
    conn, addr = server.accept()
    print('Connected by', addr, conn.getsockname()[1])
    while True:
        data = server.receive_data(conn) #Data from client

        if not data:
            break

        log.save_time()
        data_parsed = pickle.loads(data)
        data_parsed.time = log.get_time()
        data_parsed.sender = "server"
        # data_with_time = (data_parsed[0], data_parsed[1], data_parsed[2], log.get_time())

        server.send_data(server.client, pickle.dumps(data_parsed)) #Request to pc1
        res = server.receive_data(server.client, DECODE=True) #Response from pc1
        print("respuesta del pc1",res)
        log.save_time_pc1(res, data_parsed)

        server.send_data(server.client2, pickle.dumps(data_parsed)) #Request to pc2
        res2 = server.receive_data(server.client2, DECODE=True) #Response from pc2
        print("Respuesta del pc2",res2)
        log.save_time_pc2(res2, data_parsed)

        server.send_data(server.backup, pickle.dumps(data_parsed)) #Request for backup
        res_backup = server.receive_data(server.backup, DECODE=True)
        print("Respuesta del backup", res_backup)
        log.save_time_backup(res_backup, data_parsed)

        response = [res, res2, res_backup]

        log.save_logs(data_parsed, response)

        handle_response(conn,data,response, log)

        # except:
        #     print("Mensaje fallido hacia pc2")
        # try:
        #     backup.sendall((datito+"SERVERMAXIMOSUPREMO").encode())
        # except:
        #     print("mensaje fallido hacia backup")
        # print("Dato recibido:", datito)
        # if datito == "exit":
        #     conn.close()
        #     break

client.close()
client2.close()
conn.close()
