from datetime import datetime

class Log_H:
    def save_time(self, time):
        with open("timestamp", "w") as file:
            file.write(time)
    
    def read_time(self):
        with open("timestamp", "r") as file:
            timestamp_str = file.read().strip()

        # Convert back to datetime
        timestamp = datetime.fromisoformat(timestamp_str)

        print("Restored timestamp:", timestamp)


    