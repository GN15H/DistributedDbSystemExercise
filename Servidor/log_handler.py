from datetime import datetime
import json

class Log_H:
    def __init__(self):
        self.time = None
    
    def get_time(self):
        return self.time

    def _update_time(self):
        self.time = datetime.now().isoformat()

    def save_time(self):
        data = self.read_json()
        self._update_time()
        data["last_update"] = self.time
        with open("log.json", "w") as file:
            json.dump(data, file, indent=4)

    def save_time_pc1(self, response, request):
        if request.operation == "fetch":
            return None
        if response == 0:
            return None
        data = self.read_json()
        data["pc1_last_update"] = self.time
        with open("log.json", "w") as file:
            json.dump(data, file, indent=4)

    def save_time_pc2(self, response, request):
        if request.operation == "fetch":
            return None
        if response == 0:
            return None
        data = self.read_json()
        data["pc2_last_update"] = self.time
        with open("log.json", "w") as file:
            json.dump(data, file, indent=4)
    
    def save_time_backup(self, response, request):
        if request.operation == "fetch":
            return None
        if response == 0:
            return None
        data = self.read_json()
        data["backup_last_update"] = self.time
        with open("log.json", "w") as file:
            json.dump(data, file, indent=4)

    def read_json(self):
        with open("log.json", "r") as file:
            data = json.load(file)
            return data

    def get_update_times(self):
        data = self.read_json()
        return (datetime.fromisoformat(data["pc1_last_update"]), datetime.fromisoformat(data["pc2_last_update"]), datetime.fromisoformat(data["backup_last_update"]))

    def get_most_recent_updated(self):
        data = self.get_update_times()
        return max(enumerate(data), key=lambda x: x[1])

    def save_logs(self, request, response):
        if request.operation == "fetch":
            return None
        flag = True
        for item in response:
            flag = flag and (item != 0)
        if flag:
            return None
        data = self.read_json()
        data["instructions"].append(request.to_dict())
        with open("log.json", "w") as file:
            json.dump(data, file, indent=4)



'''
{
    "last_update": (datetime.now().isoformat()),
    "instructions":[
        (datetime.now(), string of instruction),
        .
        .
        .
    ]
}
'''