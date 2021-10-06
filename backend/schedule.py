import datetime
import json
import main

def get_work_setting(work):
    return list()

# 근무표 생성 함수
# consider_from_date 부터 end_date 까지의 근무를 고려하여
# start_date 부터 end_date 까지의 근무표 작성
# consider_from_date ------ start_date ------ end_date
#      (과거)                 (현재)           (미래)
def create_schedule(consider_from_date, start_date, end_date):
    total_work_list = [1, 2, 3, 4, 5, 6, 7, 8] # 모든 근무 목록
    event_list = list() # start_date부터 end_date까지의 모든 근무
    
    for work in total_work_list: # 각 근무에 대해
        work_setting_list = get_work_setting(work) # 시간대별 근무 목록
        for date in range(start_date, end_date+1): # start_date부터 end_date까지
            for work_setting in work_setting_list: # 각 시간대별로
                event = Event(date, work_setting)  # 근무 이벤트 생성 (날짜, 시간)
                event_list.append(event)           # 이벤트 목록에 추가
    
    schedule(event_list, 0)
    return

# 백트래킹으로 근무표 작성 시도
# 모든 이벤트 목록에 적합한 근무자를 채워넣으면 성공
# 다 채워넣으면 각 근무자의 누적 피로도를 계산하여 근무 불공정도를 산출
# 근무 불공정도 산출 식: max(누적 피로도) - min(누적 피로도)
# To-do: 위의 근무 불공정도 산출 식 개선
# i: i번째 event까지 처리했음을 의미
def schedule(event_list, i):
    # 모든 근무자의 누적 피로도가 동일하다면 근무 불공정도 = 0으로 최선
    # 근무 불공정도가 특정 threshold보다 낮다면 탐색을 중단하고 return
    # threshold가 너무 높으면 불공정도가 더 큰 근무표가 채택될 위험 존재
    # threshold가 너무 낮으면 탐색 시간이 너무 오래 걸릴 수 있음
    # To-do: 적절한 threshold 자동으로 산출하는 방법 찾기
    
    return