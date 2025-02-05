import datetime
import os

class timeUtils():
    def __init__(self):
        self.expires_recovery_code = int(os.getenv("EXPIRES_RECOVERY_CODE"))

    def getTime(self, timeDb):
        timeDbFormat = datetime.datetime.strptime(timeDb, "%Y-%m-%dT%H:%M:%S.%f")
        if not isinstance(timeDbFormat, datetime.datetime):
            raise ValueError("timeDbFormat must be a datetime object")

        time_now = datetime.datetime.now()
        time_diff = time_now - timeDbFormat
        elapsed_time = time_diff.total_seconds() / 60

        return elapsed_time > self.expires_recovery_code