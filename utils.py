import pandas
import time
import datetime

class CasinoUtils:

    def to_datetime(self, date:str):
        return pandas.to_datetime(date)

    def time_diff_in_hours(self, date_to_check) -> int:
        today_date = datetime.datetime.now()
        diff = today_date - date_to_check
        diff_secs = diff.total_seconds()
        diff_hours = diff_secs // 60 // 60
        return int(diff_hours)

    def time_diff_in_mins(self, start_time) -> int:
        sec_diff = time.time() - start_time
        return (sec_diff // 60)


