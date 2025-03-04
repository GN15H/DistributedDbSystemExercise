from datetime import datetime

class Log_H:
    def __init__(self):
        self.time = None
    
    def get_time(self):
        return self.time

    def _update_time(self):
        self.time = datetime.now().isoformat()

    def save_time(self):
        self._update_time()
        with open("timestamp", "w") as file:
            file.write(self.time)
