import mysql.connector

class Db_Handler:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = ""
        )
        self.cursor = self.mydb.cursor()
        self.cursor.execute("USE mibasededatos;")

    def creates_user(self, name, last_name, email, phone):
        data_user = {}
        self.cursor.execute("")
    
    def __del__(self):
        self.cursor.close()
        self.mydb.close()

cursor = mydb.cursor()

cursor.execute("USE mibasededatos;")

cursor.execute("SELECT * FROM persona;")

for item in cursor:
    print(item)

mydb.commit()
cursor.close()
mydb.close()