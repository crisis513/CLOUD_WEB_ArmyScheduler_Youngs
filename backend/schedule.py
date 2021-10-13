from copy import deepcopy
import datetime
import json
import main
from pymongo import MongoClient

def parse_time(t) -> int:
    h, m = map(int, t.split(':'))
    return h*60 + m

def get_day_worktime(start_time, end_time) -> int:
    t1 = parse_time(start_time)
    t2 = parse_time(end_time)
    t = t2 - t1
    if t <= 0:
        t += 60*24
    return t - get_night_worktime(start_time, end_time) - get_free_worktime(start_time, end_time)

def intersect_time(t1_start, t1_end, t2_start, t2_end) -> int:
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

def get_night_worktime(start_time, end_time) -> int:
    t1 = parse_time(start_time)
    t2 = parse_time(end_time)
    if t2 <= t1:
        t2 += 60*24
    night_start = parse_time('22:00')
    night_end = parse_time('06:30') + 60*24
    return intersect_time(t1, t2, night_start, night_end)

def get_free_worktime(start_time, end_time) -> int:
    t1 = parse_time(start_time)
    t2 = parse_time(end_time)
    if t2 <= t1:
        t2 += 60*24
    free_start = parse_time('18:00')
    free_end = parse_time('21:00')
    return intersect_time(t1, t2, free_start, free_end)

def get_worktime_and_fatigue(start_time, end_time) -> tuple:
    day_worktime = get_day_worktime(start_time, end_time)
    night_worktime = get_night_worktime(start_time, end_time)
    free_worktime = get_free_worktime(start_time, end_time)
    fatigue = get_fatigue_from_worktime(day_worktime, night_worktime, free_worktime)
    return (day_worktime, night_worktime, free_worktime, fatigue)

def get_fatigue_from_worktime(day_worktime, night_worktime, free_worktime) -> int:
    return day_worktime + night_worktime*2 + free_worktime*3

def int_to_date(date) -> str:
    base_date = datetime.datetime.fromisoformat('1970-01-01')
    cur_date = base_date + datetime.timedelta(days=date)
    return datetime.datetime.strftime(cur_date, '%Y-%m-%d')

def date_to_int(date) -> int:
    base_date = datetime.datetime.fromisoformat('1970-01-01')
    cur_date = datetime.datetime.fromisoformat(date)
    diff = cur_date - base_date
    return diff.days
    
class Backtrack:
    """
    백트래킹 통한 근무표 산출
    """
    def __init__(self):
        self.INF = 987654321987654321 # arbitrary large number
        self.result_schedule_list = []
        self.best_schedule = []
        self.cur_schedule = []
        self.event_list = []
        self.user_list = main.get_total_user_list()
        self.total_events = 0
        self.best_unfairness = self.INF
        self.stop_backtracking = False
        self.total_work_list = main.get_total_work_list()
        self.prev_event_list = main.get_total_event_list()

    def get_work_setting(self, work):
        return self.total_work_list[work]['work_setting']
    
    def get_prev_fatigue(self, start_date, end_date):
        start_day = date_to_int(start_date)
        end_day = date_to_int(end_date)
        for event in self.prev_event_list:
            event_day = date_to_int(event['event_date'])
            if not start_day <= event_day < end_day:
                continue
            if event['event_type'] == main.EventType.Custom:
                continue
            uid = event['userid']
            start_time = event['start_time']
            end_time = event['end_time']
            day_worktime, night_worktime, free_worktime, fatigue = get_worktime_and_fatigue(start_time, end_time)
            self.user_list[uid]['day_worktime'] += day_worktime
            self.user_list[uid]['night_worktime'] += night_worktime
            self.user_list[uid]['free_worktime'] += free_worktime
            self.user_list[uid]['fatigue'] += fatigue
            self.user_list[uid]['work_day_list'].append(event_day)

    def create_empty_event_list(self, start_date, end_date):
        start_day = date_to_int(start_date)
        end_day = date_to_int(end_date)
        for work_id in self.total_work_list:
            work_setting_list = self.get_work_setting(work_id)
            for date in range(start_day, end_day + 1):
                for work_setting in work_setting_list:
                    for _ in range(work_setting['num_workers']):
                        event = main.Events.from_scheduler(int_to_date(date), work_id, self.total_work_list[work_id]['work_name'], work_setting)
                        self.event_list.append(event)
    
    def set_event_list(self):
        # To-do: push self.event_list to DB
        return

    def schedule(self, consider_from_date, start_date, end_date):
        """
        근무표 생성 함수
        consider_from_date 부터 end_date 까지의 근무 피로도를 고려하여
        start_date 부터 end_date 까지의 근무표 작성
        consider_from_date ------ start_date ------ end_date
            (과거)                 (현재)           (미래)
        """
        self.create_empty_event_list(start_date, end_date)
        self.get_prev_fatigue(consider_from_date, start_date)
        self.total_events = len(self.event_list)
        self.unfairness = 0

        self.backtrack(0)

        for i in range(self.total_events):
            self.event_list[i]['userid'] = self.best_schedule[i]
        self.set_event_list()

    def get_unfairness(self):
        # Question: 근무 불공정도에 대한 더 좋은 척도가 있을까?
        min_fatigue = self.INF
        max_fatigue = -1
        sum_fatigue = 0
        for user in self.user_list.values():
            fatigue = user['fatigue']
            min_fatigue = min(fatigue, min_fatigue)
            max_fatigue = max(fatigue, max_fatigue)
            sum_fatigue += fatigue
        return sum_fatigue / len(self.user_list) + max_fatigue - min_fatigue

    def backtrack(self, events_idx):
        """
        events_idx: 현재 고려하는 이벤트의 인덱스
        """
        if self.stop_backtracking:
            return
        if events_idx == self.total_events:
            self.get_unfairness()
            if self.unfairness < self.best_unfairness:
                self.best_unfairness = self.unfairness
                self.best_schedule = self.cur_schedule
            self.threshold = 0
            # 근무 불공정도가 특정 threshold보다 낮다면 탐색을 중단하고 return
            # To-do: how to set threshold?
            if self.best_unfairness < self.threshold:
                self.stop_backtracking = True
                return
            # todo: end backtracking
            return

        event = self.event_list[events_idx]
        start_time = event['start_time']
        end_time = event['end_time']
        event_day = date_to_int(event['event_date'])
        work = self.total_work_list[event['work_id']]
        day_worktime, night_worktime, free_worktime, fatigue = get_worktime_and_fatigue(start_time, end_time)
        for uid, values in self.user_list.items():
            # 근무 옵션에 의해 근무 불가능한 uid는 배제
            # work_option1: 2일 연속 근무 여부
            # work_option2: 하루 쉬고 근무 여부 (e.g. 퐁당퐁당)
            # work_option3: 하루 2회 이상 근무 여부
            work_day_list = self.user_list[uid]['work_day_list']
            if work['work_option1'] == main.WorkOptionType.Never and len(work_day_list) > 0 and work_day_list[-1] >= event_day - 1:
                continue
            if work['work_option2'] == main.WorkOptionType.Never and len(work_day_list) > 0 and work_day_list[-1] >= event_day - 2:
                continue
            if work['work_option3'] == main.WorkOptionType.Never and len(work_day_list) > 0 and work_day_list[-1] == event_day:
                continue

            # 근무 옵션에 의해 선호되지 않는 근무의 경우 fatigue 추가
            # To-do: avoid hard-coded number
            additional_fatigue = 0
            if work['work_option1'] == main.WorkOptionType.NotPreferred and len(work_day_list) > 0 and work_day_list[-1] >= event_day - 1:
                additional_fatigue += 5
            if work['work_option2'] == main.WorkOptionType.NotPreferred and len(work_day_list) > 0 and work_day_list[-1] >= event_day - 2:
                additional_fatigue += 5
            if work['work_option3'] == main.WorkOptionType.NotPreferred and len(work_day_list) > 0 and work_day_list[-1] == event_day:
                additional_fatigue += 5

            self.cur_schedule.append(uid)
            self.user_list[uid]['day_worktime'] += day_worktime
            self.user_list[uid]['night_worktime'] += night_worktime
            self.user_list[uid]['free_worktime'] += free_worktime
            self.user_list[uid]['fatigue'] += (fatigue + additional_fatigue)
            self.user_list[uid]['work_day_list'].append(event_day)

            self.backtrack(events_idx + 1)

            self.cur_schedule.pop()
            self.user_list[uid]['day_worktime'] -= day_worktime
            self.user_list[uid]['night_worktime'] -= night_worktime
            self.user_list[uid]['free_worktime'] -= free_worktime
            self.user_list[uid]['fatigue'] -= (fatigue + additional_fatigue)
            self.user_list[uid]['work_day_list'].pop()

def main():
    sch = Backtrack()
    consider_from_date = '2021-10-01'
    start_date = '2021-10-13'
    end_date = '2021-10-31'
    sch.schedule(consider_from_date, start_date, end_date)

if __name__ == '__main__':
    main()