import pickle
import storage_func

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

def server_func(log, server, conn, data, db_handler, parsed_data):

        log.save_time()
        data_parsed = pickle.loads(data)
        data_parsed.time = log.get_time()
        data_parsed.sender = "server"
        # data_with_time = (data_parsed[0], data_parsed[1], data_parsed[2], log.get_time())

        client1_req = [data_parsed]
        log.get_pc1_undone_requests(client1_req)
        server.send_data(server.client, pickle.dumps(client1_req)) #Request to pc1
        res = server.receive_data(server.client, DECODE=True) #Response from pc1
        print("respuesta del pc1",res)
        log.save_time_pc1(res, client1_req)

        client2_req = [data_parsed]
        log.get_pc2_undone_requests(client2_req)
        server.send_data(server.client2, pickle.dumps(client2_req)) #Request to pc2
        res2 = server.receive_data(server.client2, DECODE=True) #Response from pc2
        print("Respuesta del pc2",res2)
        log.save_time_pc2(res2, client2_req)

        backup_res = storage_func.request_handler_client(conn=conn, db_handler=db_handler, parsed_data=parsed_data)

        response = [res, res2]

        log.save_logs(data_parsed, response)

        response.append(backup_res)
        handle_response(conn,data,response, log)

