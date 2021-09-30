from pymongo import MongoClient
import json
import logging, sys
class Users(object):
    def __init__(self, userid, passwd, en_date, de_date, now_class, unit_a, unit_b, unit_c, position, vacation, total_work_time, this_mon_work_time, prev_mon_work_time):
        self.userid = userid
        self.passwd = passwd
        self.en_date = en_date
        self.de_date = de_date
        self.now_class = now_class
        self.unit_a = unit_a
        self.unit_b = unit_b
        self.unit_c = unit_c
        self.position = position
        self.vacation = vacation
        self.total_work_time = total_work_time
        self.this_mon_work_time = this_mon_work_time
        self.prev_mon_work_time = prev_mon_work_time

class Vacation(object):
    def __init__(self, start_date, end_date, description):
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

class Works(object):
    def __init__(self, work_id, work_name, work_setting, work_option1, work_option2, work_option3, work_period):
        self.work_id = work_id
        self.work_name = work_name
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
        return Users(obj['userid'], obj['passwd'], obj['en_date'], obj['de_date'], obj['now_class'],
                     obj['unit_a'], obj['unit_b'], obj['unit_c'], obj['position'], obj['vacation'],
                     obj['total_work_time'], obj['this_mon_work_time'], obj['prev_mon_work_time'])
    elif obj['__type__'] == 'Works':
        return obj


def db_init(client):
    db = client['army_scheduler_db']
    return db

def create_user(db, userid, name, password, birth_date, en_date, de_date, now_class, unit_company, unit_platoon, unit_squad, position):
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
        'work_list': [],                # 투입 근무 목록
        'vacation': [],                 # 휴가
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

def update_user_on_userpage(db, userid, name, password, birth_date, en_date, de_date, now_class, unit_company, unit_platoon, unit_squad, position, vacation):
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
            'vacation': vacation
        }
    }
    db.Users.update_one(query, values)

def main():
    # client = MongoClient('mongodb://crlee:myPassword@20.194.38.223:3306/army_scheduler_db') # test on VM
    client = MongoClient('mongodb://localhost:27017/') # for local test
    # print(client.list_database_names())
    db = db_init(client)
    create_user(db, 'test_id', '홍길동', 'test_pw', '2000-01-01', '2021-01-01', '2022-06-30', '상병', '1중대', '2소대', '3분대', '소총수')
    create_user(db, 'test_id2', '임꺽정', 'test_pw2', '2001-01-01', '2020-10-01', '2022-03-31', '상병', '1중대', '2소대', '3분대', '소총수')
    test_user = find_user(db, 'test_id2')
    print(test_user)
    test_user = find_user(db, 'test_id')
    print(test_user)

    update_user_on_userpage(db, 'test_id', '홍길동', 'test_pw', '2000-01-01', '2021-01-01', '2022-06-30', '병장', '1중대', '2소대', '3분대', '군사과학기술병', [])
    test_user = find_user(db, 'test_id')
    print(test_user)

def clear_databases():
    client = MongoClient('mongodb://localhost:27017/') # for local test
    client.drop_database('army_scheduler_db')
    print(client.list_database_names())

if __name__ == '__main__':
    main()
