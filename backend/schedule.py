from copy import deepcopy
import datetime
import json
import main
from pymongo import MongoClient
from typing import Dict, List, Final, Tuple

def parse_time(date: main.Date, time: str) -> int:
    d = date.date
    h, m = map(int, time.split(':'))
    return d*60*24 + h*60 + m

# start_date의 start_time부터 end_date의 end_time까지 근무했을 때 주간 근무 시간 (분)
def get_day_worktime(start_date: main.Date, start_time: str, end_date: main.Date, end_time: str) -> int:
    t = parse_time(end_date, end_time) - parse_time(start_date, start_time)
    return t - get_night_worktime(start_date, start_time, end_date, end_time) - get_free_worktime(start_date, start_time, end_date, end_time)

# t1_start ~ t1_end 구간과 t2_start ~ t2_end 구간이 겹치는 시간 (분)
def intersect_time(t1_start: int, t1_end: int, t2_start: int, t2_end: int) -> int:
    assert(t1_start <= t1_end and t2_start <= t2_end)
    if t1_end <= t2_start or t2_end <= t1_start:
        return 0
    if t1_start <= t2_start <= t1_end <= t2_end:
        return t1_end - t2_start
    if t2_start <= t1_start <= t2_end <= t1_end:
        return t2_end - t1_start
    if t1_start <= t2_start <= t2_end <= t1_end:
        return t2_end - t2_start
    if t2_start <= t1_start <= t1_end <= t2_end:
        return t1_end - t1_start
    print('should not reach here')

def is_intersect(t1_start: int, t1_end: int, t2_start: int, t2_end: int) -> bool:
    assert(t1_start <= t1_end and t2_start <= t2_end)
    if t1_end < t2_start or t2_end < t1_start:
        return False
    else:
        return True

# start_date의 start_time부터 end_date의 end_time까지 근무했을 때 야간 근무 시간 (분)
def get_night_worktime(start_date: main.Date, start_time: str, end_date: main.Date, end_time: str) -> int:
    t1 = parse_time(start_date, start_time)
    t2 = parse_time(end_date, end_time)
    assert(end_date.date == start_date.date or end_date.date == start_date.date + 1)
    night_start = parse_time(start_date, '22:00')
    if end_date.date == start_date.date:
        night_end = parse_time(start_date, '24:00')
    elif end_date.isHoliday:
        night_end = parse_time(end_date, '07:00')
    else:
        night_end = parse_time(end_date, '06:30')
    return intersect_time(t1, t2, night_start, night_end)

# start_date의 start_time부터 end_date의 end_time까지 근무했을 때 개인정비시간에 근무한 시간 (분)
def get_free_worktime(start_date: main.Date, start_time: str, end_date: main.Date, end_time: str) -> int:
    t1 = parse_time(start_date, start_time)
    t2 = parse_time(end_date, end_time)
    assert(end_date.date == start_date.date or end_date.date == start_date.date + 1)
    if start_date.isHoliday:
        free1_start = parse_time(start_date, '08:00')
    else:
        free1_start = parse_time(start_date, '18:00')
    free1_end = parse_time(start_date, '21:00')
    if end_date.isHoliday:
        free2_start = parse_time(end_date, '08:00')
    else:
        free2_start = parse_time(end_date, '18:00')
    free2_end = parse_time(end_date, '21:00')
    if end_date.date == start_date.date:
        return intersect_time(t1, t2, free1_start, free1_end)
    else:
        return intersect_time(t1, t2, free1_start, free1_end) + intersect_time(t1, t2, free2_start, free2_end)

def get_worktime_and_fatigue(start_date: main.Date, start_time: str, end_date: main.Date, end_time: str) -> Tuple[int, int, int, int]:
    day_worktime = get_day_worktime(start_date, start_time, end_date, end_time)
    night_worktime = get_night_worktime(start_date, start_time, end_date, end_time)
    free_worktime = get_free_worktime(start_date, start_time, end_date, end_time)
    fatigue = get_fatigue_from_worktime(day_worktime, night_worktime, free_worktime)
    return (day_worktime, night_worktime, free_worktime, fatigue)

def get_fatigue_from_worktime(day_worktime: int, night_worktime: int, free_worktime: int) -> int:
    return day_worktime + night_worktime*2 + free_worktime*3

def int_to_date(date: int) -> str:
    base_date = datetime.datetime.fromisoformat('1970-01-01')
    cur_date = base_date + datetime.timedelta(days=date)
    return datetime.datetime.strftime(cur_date, '%Y-%m-%d')

def date_to_int(date: str) -> int:
    base_date = datetime.datetime.fromisoformat('1970-01-01')
    cur_date = datetime.datetime.fromisoformat(date)
    diff = cur_date - base_date
    return diff.days
    
class Scheduler:
    """
    백트래킹 통한 근무표 산출
    """
    def __init__(self, consider_from_date: str, start_date: str, end_date: str):
        self.consider_from_date = date_to_int(consider_from_date)
        self.start_date = date_to_int(start_date)
        self.end_date = date_to_int(end_date)

        self.INF: Final[int] = 987654321987654321 # arbitrary large number
        # self.result_schedule_list: List = []
        self.best_schedule: List[int] = [] # idx: event_idx, value: user_id
        self.cur_schedule: List[int] = [] # idx: event_idx, value: user_id

        self.date_list = main.get_date_list(self.start_date, self.end_date + 1)
        self.total_work_list = main.get_total_work_list() # key: work_id
        self.prev_event_list = main.get_event_list_within(self.consider_from_date, self.start_date)
        self.new_event_list: Dict[int, List[main.Events]] = {} # key: work_id
        self.total_user_list = main.get_total_user_list() # key: user_id
        self.num_events: Dict[int, int] = {} # key: work_id, value: number of events
        self.best_unfairness: int = self.INF
        self.stop_backtracking: bool = False
        # self.base_fatigue: Dict[int, int] = {} # key: work_id
        self.backtracking_limit: Final[int] = 100000
        self.max_events_per_schedule: Final[int] = 100000
        self.unfairness_threshold: Final[int] = 0 # To-do: any good heuristics?
        self.cnt: int = 0
        self.init_event_id()
        self.init_user_list()

    def init_event_id(self):
        max_event_id = 0
        for e in self.prev_event_list:
            max_event_id = max(max_event_id, e.event_id)
        self.event_id_prefix = (max_event_id % self.max_events_per_schedule) + 1
        self.event_id_postfix = 0

    def init_user_list(self):
        self.user_list: Dict[int, Dict[str, main.Users]] = {}
        for work_id in self.total_work_list:
            self.user_list[work_id] = {}
            for uid, user in self.total_user_list.items():
                if user.work_list[0] == work_id:
                    self.user_list[work_id][uid] = user

    def get_work_setting(self, work):
        return self.total_work_list[work].work_setting
    
    def get_prev_fatigue(self):
        for event in self.prev_event_list:
            assert(self.consider_from_date <= event.event_start_date.date < self.start_date)
            if event.event_type != main.EventType.Work:
                continue
            work_id = event.work_id
            day_worktime, night_worktime, free_worktime, fatigue = get_worktime_and_fatigue(
                start_date = event.event_start_date,
                start_time = event.event_start_time,
                end_date = event.event_end_date,
                end_time = event.event_end_time
            )
            for uid in event.user_id:
                self.user_list[work_id][uid].day_worktime += day_worktime
                self.user_list[work_id][uid].night_worktime += night_worktime
                self.user_list[work_id][uid].free_worktime += free_worktime
                self.user_list[work_id][uid].fatigue += fatigue
                # self.base_fatigue[work_id] += fatigue
                self.user_list[work_id][uid].work_day_list.append(event.event_start_date.date)

    def create_empty_event_list(self):
        for work_id, work in self.total_work_list.items():
            self.new_event_list[work_id] = []
            # self.base_fatigue[work_id] = 0
            for idx, date in enumerate(self.date_list[:-1]):
                for work_setting in work.work_setting:
                    start_time = work_setting.start_time
                    end_time = work_setting.end_time
                    if parse_time(date, end_time) <= parse_time(date, start_time):
                        end_date = self.date_list[idx + 1]
                    else:
                        end_date = date
                    day_worktime, night_worktime, free_worktime, fatigue = get_worktime_and_fatigue(date, start_time, end_date, end_time)
                    tags = []
                    tags.append(main.Tags(self.total_work_list[work_id].work_name, '#00FF00'))
                    if day_worktime > 0:
                        tags.append(main.Tags('주간근무', '#FFA500'))
                    if night_worktime > 0:
                        tags.append(main.Tags('야간근무', '#FFA500'))
                    if free_worktime > 0:
                        tags.append(main.Tags('개인정비시간근무', '#FFA500'))
                    tags.append(main.Tags(f'{work_setting.num_workers}명', "#0000FF"))
                    # self.base_fatigue[work_id] += fatigue * work_setting['num_workers']
                    for _ in range(work_setting.num_workers):
                        event_id = self.event_id_prefix * self.max_events_per_schedule + self.event_id_postfix
                        event = main.Events.from_scheduler(
                            event_id = event_id,
                            start_date = date,
                            end_date = end_date,
                            tags = tags,
                            work_id = work_id,
                            work_name = work.work_name,
                            work_setting = work_setting
                        )
                        self.event_id_postfix += 1
                        self.new_event_list[work_id].append(event)
    
    def set_event_list(self):
        result_event_list = []
        for work_id in self.new_event_list:
            for e1 in self.new_event_list[work_id]:
                exist = False
                for idx, e2 in enumerate(result_event_list):
                    if e1.event_start_date.date == e2['event_start_date']['date'] and e1.event_start_time == e2['event_start_time']:
                        exist = True
                        break
                if exist:
                    result_event_list[idx]['user_id'].append(e1.user_id[0])
                else:
                    result_event_list.append(e1.asdict())
        client = MongoClient('mongodb://localhost:27017/') # for local test
        db = main.db_init(client)
        main.insert_many_events(db, result_event_list)

    def schedule(self):
        """
        근무표 생성 함수
        consider_from_date 부터 end_date 까지의 근무 피로도를 고려하여
        start_date 부터 end_date 까지의 근무표 작성
        consider_from_date ------ start_date ------ end_date
            (과거)                 (현재)           (미래)
        """
        self.create_empty_event_list()
        self.get_prev_fatigue()
        for work_id in self.total_work_list:
            self.num_events[work_id] = len(self.new_event_list[work_id])
            self.best_unfairness = self.INF
            self.stop_backtracking = False
            # self.unfairness_threshold = 0 
            self.cnt = 0
            self.backtrack(work_id, 0)
            for i in range(self.num_events[work_id]):
                self.new_event_list[work_id][i].user_id.append(self.best_schedule[i])
        self.set_event_list()

    def get_unfairness(self, work_id):
        # Question: 근무 불공정도에 대한 더 좋은 척도가 있을까?
        min_fatigue = self.INF
        max_fatigue = -1
        # sum_fatigue = 0
        for user in self.user_list[work_id].values():
            fatigue = user.fatigue
            min_fatigue = min(fatigue, min_fatigue)
            max_fatigue = max(fatigue, max_fatigue)
            # sum_fatigue += fatigue
        # return (sum_fatigue - self.base_fatigue[work_id]) / len(self.user_list[work_id]) + max_fatigue - min_fatigue
        return max_fatigue - min_fatigue

    def backtrack(self, work_id, events_idx):
        """
        work_id: 현재 고려하는 근무
        events_idx: 현재 고려하는 이벤트의 인덱스
        """
        if self.stop_backtracking:
            return
        if events_idx == self.num_events[work_id]:
            self.unfairness = self.get_unfairness(work_id)
            self.cnt += 1
            if self.unfairness <= self.best_unfairness:
                self.best_unfairness = self.unfairness
                self.best_schedule = deepcopy(self.cur_schedule)
            # 근무 불공정도가 특정 threshold보다 낮거나 탐색을 충분히 많이 했으면 중단하고 return
            if self.best_unfairness <= self.unfairness_threshold or self.cnt >= self.backtracking_limit:
                self.stop_backtracking = True
            return

        event = self.new_event_list[work_id][events_idx]
        event_start_date = event.event_start_date
        event_start_time = event.event_start_time
        event_end_date = event.event_end_date
        event_end_time = event.event_end_time
        work = self.total_work_list[work_id]
        day_worktime, night_worktime, free_worktime, fatigue = get_worktime_and_fatigue(event_start_date, event_start_time, event_end_date, event_end_time)
        for uid in sorted(self.user_list[work_id], key=lambda x: self.user_list[work_id][x].fatigue):
            user = self.user_list[work_id][uid]

            # 근무 옵션에 의해 근무 불가능한 uid는 배제
            # work_option1: 2일 연속 근무 여부
            # work_option2: 하루 쉬고 근무 여부 (e.g. 퐁당퐁당)
            # work_option3: 하루 2회 이상 근무 여부
            if work.work_option1 == main.WorkOptionType.Never and user.last_work_day >= event_start_date.date - 1:
                continue
            if work.work_option2 == main.WorkOptionType.Never and user.last_work_day >= event_start_date.date - 2:
                continue
            if work.work_option3 == main.WorkOptionType.Never and user.last_work_day == event_start_date.date:
                continue

            # To-do: 휴가, 부대 일정, 전역 등에 의해 근무 불가능한 경우 배제
            skip = False
            for vacation in user.vacation:
                vacation_start = date_to_int(vacation.start_date)
                vacation_end = date_to_int(vacation.end_date)
                if is_intersect(vacation_start, vacation_end, event_start_date.date, event_end_date.date):
                    skip = True
                    break
            if skip:
                continue
            if date_to_int(user.de_date) <= event_start_date.date:
                continue
            
            # 근무 옵션에 의해 선호되지 않는 근무의 경우 fatigue 추가
            # To-do: avoid hard-coded number?
            additional_fatigue = 0
            if work.work_option1 == main.WorkOptionType.NotPreferred and user.last_work_day >= event_start_date.date - 1:
                additional_fatigue += 50
            if work.work_option2 == main.WorkOptionType.NotPreferred and user.last_work_day >= event_start_date.date - 2:
                additional_fatigue += 50
            if work.work_option3 == main.WorkOptionType.NotPreferred and user.last_work_day == event_start_date.date:
                additional_fatigue += 50

            self.cur_schedule.append(uid)
            user.day_worktime += day_worktime
            user.night_worktime += night_worktime
            user.free_worktime += free_worktime
            user.fatigue += (fatigue + additional_fatigue)
            tmp = user.last_work_day
            user.last_work_day = event_start_date.date

            self.backtrack(work_id, events_idx + 1)

            self.cur_schedule.pop()
            user.day_worktime -= day_worktime
            user.night_worktime -= night_worktime
            user.free_worktime -= free_worktime
            user.fatigue -= (fatigue + additional_fatigue)
            user.last_work_day = tmp

def main2():
    consider_from_date = '2021-10-01'
    start_date = '2021-10-13'
    end_date = '2021-11-12'
    sch = Scheduler(consider_from_date, start_date, end_date)
    sch.schedule()
    # print(sch.best_schedule)

if __name__ == '__main__':
    main2()