class Person:
    def __init__(self,name, last_name, email, phone):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def to_dict(self):
        return {
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone
        }