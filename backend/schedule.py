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

def get_night_worktime(start_time, end_time) -> int:
    t1 = parse_time(start_time)
    t2 = parse_time(end_time)
    night_start = parse_time('22:00')
    night_end = parse_time('06:30')
    return 0

def get_free_worktime(start_time, end_time) -> int:
    t1 = parse_time(start_time)
    t2 = parse_time(end_time)
    free_start = parse_time('18:00')
    free_end = parse_time('21:00')
    return 0

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
        self.best_score = 0
        self.stop_backtracking = False
        self.total_work_list = main.get_total_work_list()
        self.prev_event_list = main.get_total_event_list()

    def get_work_setting(self, work):
        return work['work_setting']
    
    def get_fatigue(self, start_date, end_date):
        for event in self.prev_event_list:
            uid = event['userid']
            start_time = event['start_time']
            end_time = event['end_time']
            self.user_list[uid]['day_worktime'] = get_day_worktime(start_time, end_time)
            self.user_list[uid]['night_worktime'] = get_night_worktime(start_time, end_time)
            self.user_list[uid]['free_worktime'] = get_free_worktime(start_time, end_time)

    def create_event_list(self, consider_from_date, start_date, end_date):
        for work in self.total_work_list:
            work_setting_list = self.get_work_setting(work)
            for date in range(start_date, end_date + 1): # To-do: make this for loop work somehow
                for work_setting in work_setting_list:
                    for _ in range(work_setting['num_workers']):
                        event = main.Events.from_scheduler(date, work, work_setting)
                        self.event_list.append(event)

        
    def schedule(self):
        return

# 근무표 생성 함수
# consider_from_date 부터 end_date 까지의 근무를 고려하여
# start_date 부터 end_date 까지의 근무표 작성
# consider_from_date ------ start_date ------ end_date
#      (과거)                 (현재)           (미래)
def create_schedule(consider_from_date, start_date, end_date):
    total_work_list = main.get_total_work_list() # 모든 근무 목록
    event_list = list() # start_date부터 end_date까지의 모든 근무
    
    for work in total_work_list: # 각 근무에 대해
        work_setting_list = get_work_setting(work) # 시간대별 근무 목록
        for date in range(start_date, end_date+1): # start_date부터 end_date까지
            for work_setting in work_setting_list: # 각 시간대별로
                event = Event(date, work_setting)  # 근무 이벤트 생성 (날짜, 시간)
                event_list.append(event)           # 이벤트 목록에 추가
    
    result_event_list = list()
    schedule(event_list, result_event_list, 0)
    return

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