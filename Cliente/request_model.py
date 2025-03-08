from person import Person

class Request_M:
    def __init__(self, sender, operation, person_data, time, log):
        self.sender = sender
        self.operation = operation
        self.person_data = person_data
        self.time = time
        self.log = log

    def to_dict(self):
        return {
            "sender": self.sender,
            "operation": self.operation,
            "person_data": self.person_data.to_dict(),
            "time": self.time,
            "log": self.log
        }
    
    def from_dict(data):
        return Request_M(data["sender"], data["operation"], Person.from_dict(data["person_data"]), data["time"], data["log"])
