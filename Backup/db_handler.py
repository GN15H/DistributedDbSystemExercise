import mysql.connector

class Db_Handler:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = ""
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute("USE dbbackup;")

    def create_user(self, name, last_name, email, phone):
        try: 
            add_user = ("INSERT INTO persona "
                "(nombre, apellido, correo, telefono, direccion) "
                "VALUES (%s, %s, %s, %s, 'backup')")
            data_user = (name, last_name, email, phone)
            self.cursor.execute(add_user, data_user)
            self.mydb.commit()
            return 1
        except:
            return 0

    def fetch_users(self):
        try:
            self.cursor.execute("SELECT * FROM Persona;")    
            data = []
            for item in self.cursor:
                data.append(item)
            return data
        except:
            return None


    def __del__(self):
        self.cursor.close()
        self.mydb.close()