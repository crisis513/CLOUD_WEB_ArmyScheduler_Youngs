from pymongo import MongoClient
import json
import logging, sys
from enum import enum
class Users(object):
    def __init__(self, userid, name, password, en_date, de_date, now_class, unit_company, unit_platoon, unit_squad, position, work_list, vacation, total_work_time, this_mon_work_time, prev_mon_work_time):
        self.userid = userid
        self.name = name
        self.password = password
        self.en_date = en_date
        self.de_date = de_date
        self.now_class = now_class
        self.unit_company = unit_company
        self.unit_platoon = unit_platoon
        self.unit_squad = unit_squad
        self.position = position
        self.work_list = work_list
        self.vacation = vacation
        self.total_work_time = total_work_time
        self.this_mon_work_time = this_mon_work_time
        self.prev_mon_work_time = prev_mon_work_time

class WorkTime(object):
    def __init__(self, day_worktime, night_worktime, free_worktime):
        self.day_worktime = day_worktime
        self.night_worktime = night_worktime
        self.free_worktime = free_worktime

class Vacation(object):
    def __init__(self, start_date, end_date, description):
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

class Works(object):
    def __init__(self, work_id, work_name, work_setting, work_option1, work_option2, work_option3, work_period):
        self.work_id = work_id
        self.work_name = work_name
        self.worker_list = list()
        self.work_setting = work_setting
        self.work_option1 = work_option1
        self.work_option2 = work_option2
        self.work_option3 = work_option3
        self.work_period = work_period

class WorkSetting(object):
    def __init__(self, start_time, end_time, num_workers):
        self.start_time = start_time
        self.end_time = end_time
        self.num_workers = num_workers

class EventType(enum):
    Work = 0    # 근무
    Troop = 1   # 부대 일정 (훈련 등)
    Custom = 2  # 유저 개인 일정

class Events(object):
    def __init__(self, userid, event_title, event_type, work_id, tags, event_date, event_color, start_time, end_time):
        self.userid = userid
        self.event_title = event_title
        self.event_type = event_type
        self.work_id = work_id   # 근무가 아닌 경우 -1
        self.tags = tags
        self.event_date = event_date
        self.event_color = event_color
        self.start_time = start_time
        self.end_time = end_time
    
    @classmethod
    def from_scheduler(cls, date, work_id, work_name, work_setting):
        return cls(
            userid = -1,
            event_title = work_name,
            event_type = EventType.Work,
            work_id = work_id,
            tags = Tags('some_tag_title', 'some_tag_color'),
            event_date = date,
            event_color = 'some_color',
            start_time = work_setting['start_time'],
            end_time = work_setting['end_time']
            )

class Tags(object):
    def __init__(self, tag_title, tag_color):
        self.tag_title = tag_title
        self.tag_color = tag_color

def object_decoder(obj):
    if '__type__' not in obj:
        logging.debug(f'ERROR: __type__ not in {obj}')
        return obj
    if obj['__type__'] == 'Users':
        return Users(obj['userid'], obj['name'], obj['password'], obj['birth_date'],
                     obj['en_date'], obj['de_date'], obj['now_class'],
                     obj['unit_company'], obj['unit_platoon'], obj['unit_squad'],
                     obj['position'], obj['work_list'], obj['vacation'],
                     obj['total_work_time'], obj['this_mon_work_time'], obj['prev_mon_work_time'])
    elif obj['__type__'] == 'WorkTime':
        return WorkTime(obj['day_worktime'], obj['night_worktime'], obj['free_worktime'])
    elif obj['__type__'] == 'Works':
        return Works(obj['work_id'], obj['work_name'], obj['work_setting'],
                     obj['work_option1'], obj['work_option2'], obj['work_option3'], obj['work_period'])
    elif obj['__type__'] == 'Vacation':
        return Vacation(obj['start_date'], obj['end_date'], obj['description'])
    elif obj['__type__'] == 'WorkSetting':
        return WorkSetting(obj['start_time'], obj['end_time'], obj['num_workers'])
    elif obj['__type__'] == 'Events':
        return Events(obj['userid'], obj['event_title'], obj['tags'],
                      obj['event_date'], obj['event_color'], obj['start_time'], obj['end_time'])
    elif obj['__type__'] == 'Tags':
        return Tags(obj['tag_title'], obj['tag_color'])
    else:
        logging.debug(f'ERROR: unknown __type__ {obj["__type__"]}')
        return obj

def db_init(client):
    db = client['army_scheduler_db']
    return db

def create_user(db, userid, name, password, birth_date, en_date, de_date, now_class, unit_company, unit_platoon, unit_squad, position, work_list, vacation):
    user = {
        'userid': userid,               # 아이디
        'name': name,                   # 이름
        'password': password,           # 패스워드
        'birth_date' : birth_date,      # 생년월일
        'en_date': en_date,             # 입대일
        'de_date': de_date,             # 전역일
        'now_class': now_class,         # 현 계급
        'unit_company': unit_company,   # 중대
        'unit_platoon': unit_platoon,   # 소대
        'unit_squad': unit_squad,       # 분대
        'position': position,           # 보직
        'work_list': work_list,         # 투입 근무 목록
        'vacation': vacation,           # 휴가
        'total_work_time': {            # 총 근무 시간 (분)
            'work_time': 0,
            'sleep_time': 0,
            'personal_time': 0
        },
        'this_mon_work_time': {         # 이번 달 근무 시간 (분)
            'work_time': 0,
            'sleep_time': 0,
            'personal_time': 0
        },
        'prev_mon_work_time': {         # 지난 달 근무 시간 (분)
            'work_time': 0,
            'sleep_time': 0,
            'personal_time': 0
        }
    }
    return db.Users.insert_one(user).inserted_id

def find_user(db, uid):
    query = { 'userid': uid }
    return db.Users.find_one(query)

def update_user_on_userpage(db, userid, name, password, birth_date, en_date, de_date, now_class, unit_company, unit_platoon, unit_squad, position, work_list, vacation):
    query = { 'userid': userid }
    values = {
        '$set': {
            'name': name,
            'password': password,
            'birth_date': birth_date,
            'en_date': en_date,
            'de_date': de_date,
            'now_class': now_class,
            'unit_company': unit_company,
            'unit_platoon': unit_platoon,
            'unit_squad': unit_squad,
            'position': position,
            'work_list': work_list,
            'vacation': vacation
        }
    }
    db.Users.update_one(query, values)

def create_work(db, work_id, work_name, work_setting, work_option1, work_option2, work_option3, work_period):
    work = {
        'work_id': work_id,             # 일련번호
        'work_name': work_name,         # 근무명
        'work_setting': work_setting,   # 근무설정
        'work_option1': work_option1,   # 근무옵션1
        'work_option2': work_option2,   # 근무옵션2
        'work_option3': work_option3,   # 근무옵션3
        'work_period': work_period      # 근무주기
    }
    return db.Works.insert_one(work).inserted_id

def update_work(db, work_id, work_name, work_setting, work_option1, work_option2, work_option3, work_period):
    query = { 'work_id': work_id }
    values = {
        '$set': {
            'work_name': work_name,         # 근무명
            'work_setting': work_setting,   # 근무설정
            'work_option1': work_option1,   # 근무옵션1
            'work_option2': work_option2,   # 근무옵션2
            'work_option3': work_option3,   # 근무옵션3
            'work_period': work_period      # 근무주기
        }
    }
    db.Works.update_one(query, values)

def find_work(db, work_id):
    query = { 'work_id': work_id }
    return db.Works.find_one(query)

def create_event(db, userid, event_title, tags, event_date, event_color, start_time, end_time):
    event = {
        'userid': userid,
        'event_title': event_title,
        'tags': tags,
        'event_date': event_date,
        'event_color': event_color,
        'start_time': start_time,
        'end_time': end_time
    }
    return db.Events.insert_one(event).inserted_id

def dbtest():
    clear_databases()
    dbtest1()
    dbtest2()

def dbtest1():
    # client = MongoClient('mongodb://crlee:myPassword@20.194.38.223:3306/army_scheduler_db') # test on VM
    client = MongoClient('mongodb://localhost:27017/') # for local test
    # print(client.list_database_names())
    db = db_init(client)
    # db, userid, name, password, birth_date, en_date, de_date, now_class, unit_company, unit_platoon, unit_squad, position, work_list, vacation
    create_user(db, 'test_id', '홍길동', 'test_pw', '2000-01-01', '2021-01-01', '2022-06-30', '상병', '1중대', '2소대', '3분대', '소총수', [1], [])
    create_user(db, 'test_id2', '임꺽정', 'test_pw2', '2001-01-01', '2020-10-01', '2022-03-31', '상병', '1중대', '2소대', '3분대', '소총수', [1], [])
    test_user = find_user(db, 'test_id2')
    print(test_user)
    test_user = find_user(db, 'test_id')
    print(test_user)

    update_user_on_userpage(db, 'test_id', '홍길동', 'test_pw', '2000-01-01', '2021-01-01', '2022-06-30', '병장', '1중대', '2소대', '3분대', '군사과학기술병', [], [])
    test_user = find_user(db, 'test_id')
    print(test_user)

def dbtest2():
    client = MongoClient('mongodb://localhost:27017/')
    db = db_init(client)
    create_work(db, 1, '불침번', [{'start_time':'22:00', 'end_time':'24:00', 'num_workers':2}], 1, 1, 1, 1)
    create_work(db, 2, '당직', [{'start_time':'09:00', 'end_time':'08:59', 'num_workers':1}], 2, 2, 2, 1)
    test_work = find_work(db, 1)
    print(test_work)
    test_work = find_work(db, 2)
    print(test_work)

    update_work(db, 1, '불침번', [{'start_time':'24:00', 'end_time':'02:00', 'num_workers':2}], 3, 3, 3, 1)
    test_work = find_work(db, 1)
    print(test_work)

def clear_databases():
    client = MongoClient('mongodb://localhost:27017/') # for local test
    client.drop_database('army_scheduler_db')
    print(client.list_database_names())

def get_total_work_list():
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    works = db.Works.find()
    work_dict = {}
    for w in works:
        work_dict[w['work_id']] = {
            'work_name': w['work_name'],
            'work_setting': w['work_setting'],
            'work_option1': w['work_option1'],
            'work_option2': w['work_option2'],
            'work_option3': w['work_option3'],
            'work_period': w['work_period']
        }
    return work_dict

def get_total_event_list():
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    events = db.Events.find()
    return events

def get_total_user_list():
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    users = db.Users.find()
    user_dict = {}
    for u in users:
        user_dict[u['userid']] = {'day_worktime':0, 'night_worktime':0, 'free_worktime':0, 'fatigue':0, 'work_day_list':[]}
    return user_dict

def main():
    works = get_total_work_list()
    for w in works:
        print(w)

if __name__ == '__main__':
    main()
