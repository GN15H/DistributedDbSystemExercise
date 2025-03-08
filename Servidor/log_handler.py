from datetime import datetime
from request_model import Request_M
import json

class Log_H:
    def __init__(self):
        self.time = None
    
    def get_time(self):
        return self.time

    def _update_time(self):
        self.time = datetime.now().isoformat()

    def _avoid_duplicates(self):
        data = self.read_json()
        for instruction in data["instructions"]:
            if instruction["time"] == data["last_update"]:
                return True
        return False
        #si hay alguna con tiempo igual al last updated assert

    def update_json(self, json_data):
        with open("log.json", "w") as file:
            json.dump(json_data, file, indent=4)

    def save_time(self):
        data = self.read_json()
        self._update_time()
        data["last_update"] = self.time
        with open("log.json", "w") as file:
            json.dump(data, file, indent=4)

    def save_time_pc1(self, response, request_arr):
        for request in request_arr:
            if request.operation == "fetch":
                continue
            if response == 0:
                return None
            data = self.read_json()
            data["pc1_last_update"] = self.time
            with open("log.json", "w") as file:
                json.dump(data, file, indent=4)

    def save_time_pc2(self, response, request_arr):
        for request in request_arr:
            if request.operation == "fetch":
                continue
            if response == 0:
                continue
            data = self.read_json()
            data["pc2_last_update"] = self.time
            with open("log.json", "w") as file:
                json.dump(data, file, indent=4)
    
    def save_time_backup(self, response, request_arr):
        for request in request_arr:
            if request.operation == "fetch":
                continue
            if response == 0:
                continue
            data = self.read_json()
            data["backup_last_update"] = self.time
            with open("log.json", "w") as file:
                json.dump(data, file, indent=4)
                
    def save_time_backup_2(self, response, request_arr):
        data = self.read_json()
        data["backup_last_update"] = datetime.now().isoformat()
        with open("log.json", "w") as file:
            json.dump(data, file, indent=4)
                
    def read_json(self):
        with open("log.json", "r") as file:
            data = json.load(file)
            return data

    def get_update_times(self):
        data = self.read_json()
        return (datetime.fromisoformat(data["pc1_last_update"]), datetime.fromisoformat(data["pc2_last_update"]), datetime.fromisoformat(data["backup_last_update"]))

    def get_most_recent_updated(self, response):
        data = self.get_update_times()
        dates_with_index = sorted(enumerate(data),key= lambda x: x[1],reverse=True)
        
        for item in dates_with_index:
            if response[item[0]] != 0:
                return item[0], 0
        return 0, 0
        # return max(enumerate(data), key=lambda x: x[1])
    
    def handle_backup_log(self, backup_log):
        if backup_log == 0:
            return None
        current_log = self.read_json()
        if datetime.fromisoformat(current_log["last_update"]) >= datetime.fromisoformat(backup_log["last_update"]):
            return None
        current_log["pc1_last_update"] = backup_log["pc1_last_update"]
        current_log["pc2_last_update"] = backup_log["pc2_last_update"]
        current_log["backup_last_update"] = backup_log["last_update"]
        current_log["instructions"].extend(backup_log["instructions"])
        self.update_json(current_log)

    def save_logs(self, request, response):
        if request.operation == "fetch":
            return None
        flag = True
        for item in response:
            flag = flag and (item != 0)
        if flag:
            data = self.read_json()
            data["instructions"] = []
            self.update_json(data)
            return None
        if self._avoid_duplicates():
            return None
        data = self.read_json()
        data["instructions"].append(request.to_dict())
        with open("log.json", "w") as file:
            json.dump(data, file, indent=4)

    def get_undone_requests(self, time, requests_arr):
        data = self.read_json()
        for instruction in data["instructions"]:
            if datetime.fromisoformat(instruction["time"]) > time:
                requests_arr.append(Request_M.from_dict(instruction))

    def get_pc1_undone_requests(self, request_arr):
        data = self.get_update_times()
        self.get_undone_requests(data[0],request_arr)
    def get_pc2_undone_requests(self, request_arr):
        data = self.get_update_times()
        self.get_undone_requests(data[1],request_arr)
    def get_backup_undone_requests(self, request_arr):
        data = self.get_update_times()
        self.get_undone_requests(data[2],request_arr)


'''
{
    "last_update": (datetime.now().isoformat()),
    "pc1_last_update": ||,
    "pc2_last_update": ||,
    "backup_last_update": ||,
    "instructions":[
        (datetime.now(), string of instruction),
        .
        .
        .
    ]
}
'''