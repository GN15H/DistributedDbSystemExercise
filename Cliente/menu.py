from person import Person
from request_model import Request_M
import pickle

def menu():
    print("0. Salir")
    print("1. Obtener usuarios")
    print("2. Crear usuario")
    option = int(input())
    if option == 0:
        return Request_M("client","exit",Person("","","",""),None)
    elif option == 1:
        return Request_M("client","fetch",Person("","","",""),None)
    elif option == 2:
        return create_user()
    else:
        return Request_M("client","exit",Person("","","",""),None)

def create_user():
    name = str(input("Ingrese nombre de la persona\n"))
    last_name = str(input("Ingrese apellido de la persona\n"))
    email = str(input("Ingrese email de la persona\n"))
    phone = str(input("Ingrese el telefono de la persona\n"))
    return Request_M("client","create",Person(name,last_name,email,phone),None)

def handle_response(data, response):
    if not response:
        print("Hubo un problema de conexión")
        return None
    data_body = pickle.loads(response)
    if data.operation == "create":
        print("Registro exitoso\n" if data_body else "Fallo al crear registro\n")
        print("\n")
    if data.operation == "fetch":
        print(data_body,"\n")
        print("\n")
        
