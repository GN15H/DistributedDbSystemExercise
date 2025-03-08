class Person:
    def __init__(self,name, last_name, email, phone):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def from_dict(data):
        return Person(data["name"], data["last_name"], data["email"], data["phone"])