import datetime
from pytz import timezone
import form
from algorithm import form
# import schedule
from pymongo import MongoClient
from typing import List, Tuple

def get_ymd(date: str) -> Tuple[int, int, int]:
    return tuple(map(int, date.split('-')))

def get_last_month(date: datetime.datetime) -> datetime.datetime:
    first = date.replace(day = 1)
    return first - datetime.timedelta(days = 1)

class Statistics:
    def __init__(self, user_id: str):
        self.client = MongoClient('mongodb://localhost:27017/') # for local test
        self.db = self.client['army_scheduler_db']
        self.user_id = user_id
        self.user = self.get_user()
        self.now = datetime.datetime.now(timezone('Asia/Seoul'))
        self.last_month = get_last_month(self.now)

    def get_user(self) -> form.Users:
        user = form.Users.from_dict(self.db.Users.find_one({'user_id': self.user_id}))
        user.prev_month_worked_time = form.WorkTime(0, 0, 0)
        user.this_month_worked_time = form.WorkTime(0, 0, 0)
        user.this_month_work_time_left = form.WorkTime(0, 0, 0)
        user.total_worked_time = form.WorkTime(0, 0, 0)
        return user

    def get_event_list(self) -> List[form.Events]:
        events = self.db.Events.find({'user_id': self.user_id})
        return [form.Events.from_dict(e) for e in events]

    def update_user_stat(self):
        event_list = self.get_event_list()
        for event in event_list:
            day_worktime, night_worktime, free_worktime, _ = schedule.get_worktime_and_fatigue(
                event.event_start_date,
                event.event_start_time,
                event.event_end_date,
                event.event_end_time
            )
            year, month, _ = get_ymd(event.event_start_date.date_string)
            _, _, day = get_ymd(event.event_end_date.date_string)
            event_end = datetime.datetime.strptime(
                event.event_end_date.date_string + ' ' + event.event_end_time,
                '%Y-%m-%d %H:%M'
            ).astimezone(timezone('Asia/Seoul'))
            if year == self.now.year and month == self.now.month and event_end < self.now:
                self.user.this_month_worked_time.day_worktime += day_worktime
                self.user.this_month_worked_time.night_worktime += night_worktime
                self.user.this_month_worked_time.free_worktime += free_worktime
            if year == self.now.year and month == self.now.month and event_end >= self.now:
                self.user.this_month_work_time_left.day_worktime += day_worktime
                self.user.this_month_work_time_left.night_worktime += night_worktime
                self.user.this_month_work_time_left.free_worktime += free_worktime
            if year == self.last_month.year and month == self.last_month.month:
                self.user.prev_month_worked_time.day_worktime += day_worktime
                self.user.prev_month_worked_time.night_worktime += night_worktime
                self.user.prev_month_worked_time.free_worktime += free_worktime
            if event_end < self.now:
                self.user.total_worked_time.day_worktime += day_worktime
                self.user.total_worked_time.night_worktime += night_worktime
                self.user.total_worked_time.free_worktime += free_worktime
        self.db.Users.update_one(
            { 'user_id': self.user.user_id },
            {
                '$set': {
                    'prev_month_worked_time': self.user.prev_month_worked_time.asdict(),
                    'this_month_worked_time': self.user.this_month_worked_time.asdict(),
                    'this_month_work_time_left': self.user.this_month_work_time_left.asdict(),
                    'total_worked_time': self.user.total_worked_time.asdict()
                }
            }
        )

if __name__ == '__main__':
    for i in range(50):
        user_id = 'u' + str(i)
        s = Statistics(user_id)
        s.update_user_stat()
    users = form.get_total_user_list()
    for user in users.values():
        print(user.user_id, user.name, user.prev_month_worked_time.asdict(), user.this_month_worked_time.asdict(), user.this_month_work_time_left.asdict(), user.total_worked_time.asdict())