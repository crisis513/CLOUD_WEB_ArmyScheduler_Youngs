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
        self.event_list = {}
        self.total_user_list = main.get_total_user_list()
        self.total_events = {}
        self.best_unfairness = self.INF
        self.stop_backtracking = False
        self.base_fatigue = {}
        self.backtracking_limit = 100000
        self.unfairness_threshold = 0
        self.cnt = 0
        self.total_work_list = main.get_total_work_list()
        self.prev_event_list = main.get_total_event_list()
        self.init_event_id()
        self.init_user_list()
    
    def init_user_list(self):
        self.user_list = {}
        for work_id in self.total_work_list:
            self.user_list[work_id] = {}
            for uid, user in self.total_user_list.items():
                if user['work'][0] == work_id:
                    self.user_list[work_id][uid] = user

    def init_event_id(self):
        self.magic = 100000
        max_event_id = 0
        for e in self.prev_event_list:
            max_event_id = max(max_event_id, e['event_id'])
        self.event_id_prefix = (max_event_id % self.magic) + 1
        self.event_id_postfix = 0

    def get_work_setting(self, work):
        return self.total_work_list[work]['work_setting']
    
    def get_prev_fatigue(self, start_date, end_date):
        start_day = date_to_int(start_date)
        end_day = date_to_int(end_date)
        for event in self.prev_event_list:
            event_day = date_to_int(event['event_date'])
            if not start_day <= event_day < end_day:
                continue
            if event['event_type'] != main.EventType.Work:
                continue
            uid = event['userid']
            start_time = event['start_time']
            end_time = event['end_time']
            work_id = event['work_id']
            day_worktime, night_worktime, free_worktime, fatigue = get_worktime_and_fatigue(start_time, end_time)
            self.user_list[work_id][uid]['day_worktime'] += day_worktime
            self.user_list[work_id][uid]['night_worktime'] += night_worktime
            self.user_list[work_id][uid]['free_worktime'] += free_worktime
            self.user_list[work_id][uid]['fatigue'] += fatigue
            self.base_fatigue[work_id] += fatigue
            self.user_list[work_id][uid]['work_day_list'].append(event_day)

    def create_empty_event_list(self, start_date, end_date):
        start_day = date_to_int(start_date)
        end_day = date_to_int(end_date)
        for work_id in self.total_work_list:
            self.event_list[work_id] = []
            self.base_fatigue[work_id] = 0
            work_setting_list = self.get_work_setting(work_id)
            for date in range(start_day, end_day + 1):
                for work_setting in work_setting_list:
                    start_time = work_setting['start_time']
                    end_time = work_setting['end_time']
                    day_worktime, night_worktime, free_worktime, fatigue = get_worktime_and_fatigue(start_time, end_time)
                    # TODO: tag 정보 추가
                    # app/models/event.py line 18 부터 참조하여 리스트 형태로 집어넣을 것
                    # 고민거리: 마지막 태그는 인원 수? 근무 인원 명단?
                    tags = []
                    tags.append(main.Tags(self.total_work_list[work_id]['work_name'], 'green'))
                    if day_worktime > 0:
                        tags.append(main.Tags('주간근무', 'orange'))
                    if night_worktime > 0:
                        tags.append(main.Tags('야간근무', 'orange'))
                    if free_worktime > 0:
                        tags.append(main.Tags('개인정비시간근무', 'orange'))
                    # tags.append(근무 인원 정보)
                    self.base_fatigue[work_id] += fatigue * work_setting['num_workers']
                    for _ in range(work_setting['num_workers']):
                        event_id = self.event_id_prefix * self.magic + self.event_id_postfix
                        # TODO: Events.from_scheduler에 tag 넣게 수정
                        event = main.Events.from_scheduler(event_id, int_to_date(date), work_id, self.total_work_list[work_id]['work_name'], work_setting)
                        self.event_id_postfix += 1
                        self.event_list[work_id].append(event)
    
    def set_event_list(self):
        # To-do: push self.event_list to DB
        event_list = []
        for work_id in self.event_list:
            for event in self.event_list[work_id]:
                event_list.append(event.asdict())
        print(event_list)
        client = MongoClient('mongodb://localhost:27017/') # for local test
        db = main.db_init(client)
        main.insert_many_events(db, event_list)

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
        for work_id in self.total_work_list:
            self.total_events[work_id] = len(self.event_list[work_id])
            self.best_unfairness = self.INF
            self.stop_backtracking = False
            self.unfairness_threshold = 0 # To-do: any good heuristics?
            self.cnt = 0
            self.backtrack(work_id, 0)
            for i in range(self.total_events[work_id]):
                self.event_list[work_id][i].userid = self.best_schedule[i]
        self.set_event_list()

    def get_unfairness(self, work_id):
        # Question: 근무 불공정도에 대한 더 좋은 척도가 있을까?
        min_fatigue = self.INF
        max_fatigue = -1
        sum_fatigue = 0
        for user in self.user_list[work_id].values():
            fatigue = user['fatigue']
            min_fatigue = min(fatigue, min_fatigue)
            max_fatigue = max(fatigue, max_fatigue)
            sum_fatigue += fatigue
        # return (sum_fatigue - self.base_fatigue[work_id]) / len(self.user_list[work_id]) + max_fatigue - min_fatigue
        return max_fatigue - min_fatigue

    def backtrack(self, work_id, events_idx):
        """
        work_id: 현재 고려하는 근무
        events_idx: 현재 고려하는 이벤트의 인덱스
        """
        if self.stop_backtracking:
            return
        if events_idx == self.total_events[work_id]:
            self.unfairness = self.get_unfairness(work_id)
            self.cnt += 1
            if self.unfairness <= self.best_unfairness:
                self.best_unfairness = self.unfairness
                self.best_schedule = deepcopy(self.cur_schedule)
            # 근무 불공정도가 특정 threshold보다 낮거나 탐색을 충분히 많이 했으면 중단하고 return
            if self.best_unfairness <= self.unfairness_threshold or self.cnt >= self.backtracking_limit:
                self.stop_backtracking = True
            return

        event = self.event_list[work_id][events_idx]
        start_time = event.start_time
        end_time = event.end_time
        event_day = date_to_int(event.event_date)
        work = self.total_work_list[work_id]
        day_worktime, night_worktime, free_worktime, fatigue = get_worktime_and_fatigue(start_time, end_time)
        for uid in sorted(self.user_list[work_id], key=lambda x: self.user_list[work_id][x]['fatigue']):
            user = self.user_list[work_id][uid]

            # 근무 옵션에 의해 근무 불가능한 uid는 배제
            # work_option1: 2일 연속 근무 여부
            # work_option2: 하루 쉬고 근무 여부 (e.g. 퐁당퐁당)
            # work_option3: 하루 2회 이상 근무 여부
            work_day_list = user['work_day_list']
            if work['work_option1'] == main.WorkOptionType.Never and len(work_day_list) > 0 and work_day_list[-1] >= event_day - 1:
                continue
            if work['work_option2'] == main.WorkOptionType.Never and len(work_day_list) > 0 and work_day_list[-1] >= event_day - 2:
                continue
            if work['work_option3'] == main.WorkOptionType.Never and len(work_day_list) > 0 and work_day_list[-1] == event_day:
                continue

            # To-do: 휴가, 부대 일정, 전역 등에 의해 근무 불가능한 경우 배제

            # 근무 옵션에 의해 선호되지 않는 근무의 경우 fatigue 추가
            # To-do: avoid hard-coded number?
            additional_fatigue = 0
            if work['work_option1'] == main.WorkOptionType.NotPreferred and len(work_day_list) > 0 and work_day_list[-1] >= event_day - 1:
                additional_fatigue += 5
            if work['work_option2'] == main.WorkOptionType.NotPreferred and len(work_day_list) > 0 and work_day_list[-1] >= event_day - 2:
                additional_fatigue += 5
            if work['work_option3'] == main.WorkOptionType.NotPreferred and len(work_day_list) > 0 and work_day_list[-1] == event_day:
                additional_fatigue += 5

            self.cur_schedule.append(uid)
            user['day_worktime'] += day_worktime
            user['night_worktime'] += night_worktime
            user['free_worktime'] += free_worktime
            user['fatigue'] += (fatigue + additional_fatigue)
            user['work_day_list'].append(event_day)

            self.backtrack(work_id, events_idx + 1)

            self.cur_schedule.pop()
            user['day_worktime'] -= day_worktime
            user['night_worktime'] -= night_worktime
            user['free_worktime'] -= free_worktime
            user['fatigue'] -= (fatigue + additional_fatigue)
            user['work_day_list'].pop()

def main2():
    sch = Backtrack()
    consider_from_date = '2021-10-01'
    start_date = '2021-10-13'
    end_date = '2021-11-12'
    sch.schedule(consider_from_date, start_date, end_date)
    # print(sch.best_schedule)

if __name__ == '__main__':
    main2()