import pickle

def request_handler_client(conn, db_handler, parsed_data):
    res = True
    for request in parsed_data:
        if request.operation == "create":
            res = res and db_handler.create_user(request.person_data.name, request.person_data.last_name, request.person_data.email, request.person_data.phone)
        elif request.operation == "fetch" and len(parsed_data) == 1:
            res = res and db_handler.fetch_users()
    print("Respuesta",res)
    return res
    # conn.sendall(pickle.dumps(res))

def request_handler_server(conn, db_handler, parsed_data):
    res = True
    for request in parsed_data:
        if request.operation == "create":
            res = res and db_handler.create_user(request.person_data.name, request.person_data.last_name, request.person_data.email, request.person_data.phone)
        elif request.operation == "fetch" and len(parsed_data) == 1:
            res = res and db_handler.fetch_users()
    print("Respuesta",res)
    conn.sendall(pickle.dumps(res))