from pymongo import MongoClient
import json
import logging, sys
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

class Events(object):
    def __init__(self, userid, event_title, tags, event_date, event_color, start_time, end_time):
        self.userid = userid
        self.event_title = event_title
        self.tags = tags
        self.event_date = event_date
        self.event_color = event_color
        self.start_time = start_time
        self.end_time = end_time

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