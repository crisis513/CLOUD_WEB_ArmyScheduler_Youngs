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
        self.result_schedule_list = []
        self.best_schedule = []
        self.cur_schedule = []
        self.event_list = []
        self.user_list = main.get_total_user_list()
        self.total_events = 0
        self.best_unfairness = 0
        self.stop_backtracking = False
        self.total_work_list = main.get_total_work_list()
        self.prev_event_list = main.get_total_event_list()

    def get_work_setting(self, work):
        return work['work_setting']
    
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
        for work in self.total_work_list:
            work_setting_list = self.get_work_setting(work)
            for date in range(start_day, end_day + 1):
                for work_setting in work_setting_list:
                    for _ in range(work_setting['num_workers']):
                        event = main.Events.from_scheduler(int_to_date(date), work, work_setting)
                        self.event_list.append(event)

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
        # To-do: now push this results back to DB
    
    def backtrack(self, events_idx):
        """
        events_idx: 현재 고려하는 이벤트의 인덱스
        """
        if self.stop_backtracking:
            return
        if events_idx == self.total_events:
            return
            # end backtracking
        event = self.event_list[events_idx]
        for uid, values in self.user_list.items():
            # todo: 근무 옵션을 보고 현재 uid를 거를지 판단
            # todo: 추가한다면 event에 uid 추가 후 다음 backtrack 호출
            # todo: backtrack 종료 후 uid 다시 제거

# 백트래킹으로 근무표 작성 시도
# 모든 이벤트 목록에 적합한 근무자를 채워넣는데 성공했다면...
    # result_event_list가 빈 리스트라면 이를 갱신
    # 아니라면 두 근무표의 근무 불공정도를 비교해 작은 쪽을 result_event_list로 설정
# 근무 불공정도 산출 식: max(누적 피로도) - min(누적 피로도)
# To-do: 위의 근무 불공정도 산출 식 개선
# i: i번째 event까지 처리했음을 의미
def schedule(event_list, result_event_list, i):
    # 모든 근무자의 누적 피로도가 동일하다면 근무 불공정도 = 0으로 최선
    # 근무 불공정도가 특정 threshold보다 낮다면 탐색을 중단하고 return
    # threshold가 너무 높으면 불공정도가 더 큰 근무표가 채택될 위험 존재
    # threshold가 너무 낮으면 탐색 시간이 너무 오래 걸릴 수 있음
    # To-do: 적절한 threshold 자동으로 산출하는 방법 찾기
    if i == LAST_EVENT_IDX:
        return

def unfairness(event_list):
    return max(event_list) - min(event_list)