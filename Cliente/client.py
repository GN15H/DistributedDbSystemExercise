import menu
import pickle
import connection_client
import sys

client = connection_client.Connection()
while True:
    data = menu.menu()
    client.send_data(pickle.dumps(data))
    response = client.receive_data()
    menu.handle_response(data,response)
    if data == "exit":
        break
client.close()