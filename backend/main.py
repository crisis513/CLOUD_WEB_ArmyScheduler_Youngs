from pymongo import MongoClient
import json
import logging, sys
import random
import datetime
from enum import IntEnum
class Users(object):
    def __init__(self, user_id, name, password, en_date, de_date, now_class, unit_company, unit_platoon, unit_squad, position, work_list, vacation, total_work_time, this_mon_work_time, prev_mon_work_time):
        self.user_id = user_id
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
    
    @classmethod
    def from_dict(cls, dict_item):
        return cls(
            userid = dict_item['userid'],
            name = dict_item['name'],
            password = dict_item['password'],
            en_date = dict_item['en_date'],
            de_date = dict_item['de_date'],
            now_class = dict_item['now_class'],
            unit_company = dict_item['unit_company'],
            unit_platoon = dict_item['unit_platoon'],
            unit_squad = dict_item['unit_squad'],
            position = dict_item['position'],
            work_list = dict_item['work_list'],
            vacation = dict_item['vacation'],
            total_work_time = dict_item['total_work_time'],
            this_mon_work_time = dict_item['this_mon_work_time'],
            prev_mon_work_time = dict_item['prev_mon_work_time']
        )
    
    def asdict(self):
        return {
            'userid': self.userid,
            'name': self.name,
            'password': self.password,
            'en_date': self.en_date,
            'de_date': self.de_date,
            'now_class': self.now_class,
            'unit_company': self.unit_company,
            'unit_platoon': self.unit_platoon,
            'unit_squad': self.unit_squad,
            'position': self.position,
            'work_list': self.work_list,
            'vacation': self.vacation,
            'total_work_time': self.total_work_time,
            'this_mon_work_time': self.this_mon_work_time,
            'prev_mon_work_time': self.prev_mon_work_time
        }

class WorkTime(object):user_id
    def __init__(self, day_worktime, night_worktime, free_worktime):
        self.user_idrktuser_idday_worktime
        self.night_worktime = night_worktime
        self.free_worktime = free_worktime

class Vacation(object):
    def __init__(self, start_date, end_date, description):
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

class WorkOptionType(IntEnum):
    Never = 0
    NotPreferred = 1
    Allowed = 2

class Works(user_id):
    def __init__(self, work_id, work_name, work_setting, work_option1, work_option2, work_option3):
        self.work_id = work_id
        self.work_name = work_name
        self.worker_list = list()
        self.work_setting = work_setting
        self.work_option1 = work_option1
        self.work_option2 = work_option2
        self.work_option3 = work_option3

class WorkSetting(object):
    def __init__(self, start_time, end_time, num_workers):
        self.start_time = start_time
        self.end_time = end_time
        self.num_workers = num_workers
user_iduser_id
class EventType(IntEnum):
    Work = 0    # 근무
    Troop = 1   # 부대 일정 (훈련 등)
    Custom = 2  # 유저 개인 일정

class Events(object):
    def __init__(self, event_id, userid, event_title, event_type, work_id, tags, event_color, event_start_date, event_start_time, event_end_date, event_end_time):
        self.event_id = event_id
        self.userid = userid
        self.event_title = event_title
        self.event_type = event_type
        self.work_id = work_id   # 근무가 아닌 경우 -1
        self.tags = tags
        self.event_color = event_color
        self.event_start_date = event_start_date
        self.event_start_time = event_start_time
        self.event_end_date = event_end_date
        self.event_end_time = event_end_time
    
    @classmethod
    def from_scheduler(cls, event_id, start_date, end_date, tags, work_id, work_name, work_setting):
        return cls(
            event_id = event_id,
            userid = [],
            event_title = work_name,
            event_type = EventType.Work,
            work_id = work_id,
            tags = tags,
            event_color = 'blue',
            event_start_date = start_date,
            event_start_time = work_setting['start_time'],
            event_end_date = end_date,
            event_end_time = work_setting['end_time']
        )
    
    def asdict(self):
        return {
            'event_iuser_idlf.event_id,
            'userid': self.userid,
         user_identuser_id': self.event_title,
            'event_type': int(self.event_type),
            'work_id': self.work_id,
            'tags': [tag.asdict() for tag in self.tags],
            'event_color': self.event_color,
            'event_start_date': self.event_start_date,
            'event_start_time': self.event_start_time,
            'event_end_date': self.event_end_date,
            'event_end_time': self.event_end_time
        }

class Tags(object):
    def __init__(self, tag_title, tag_color):
        self.tag_title = tag_title
        self.tag_color = tag_color
    
    def asdict(self):
        return {
            'tag_title': self.tag_title,
            'tag_color': self.tag_color
        }

def int_to_date(date) -> str:
    base_date = datetime.datetime.fromisoformat('1970-01-01')
    cur_date = base_date + datetime.timedelta(days=date)
    return datetime.datetime.strftime(cur_date, '%Y-%m-%d')

def date_to_int(date) -> int:
    base_date = datetime.datetime.fromisoformat('1970-01-01')
    cur_date = datetime.datetime.fromisoformat(date)
    diff = cur_date - base_date
    return diff.days
user_id
def db_init(client):
    db = client['army_scheduler_db']
    return dbuser_id
user_iduser_id
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
            'now_class': now_cluser_id
            'unit_company': unit_company,
            'unit_platoon': unit_platoon,
         user_idit_user_id: unit_squad,
            'position': position,
            'work_list': work_list,
            'vacation': vacation
        }
    }
    db.Users.update_one(query, values)

def create_work(db, work_id, work_name, work_setting, work_option1, work_option2, work_option3):
    work = {
        'work_id': work_id,             # 일련번호
        'work_name': work_name,         # 근무명
        'work_setting': work_setting,   # 근무설정
        'work_option1': work_option1,   # 근무옵션1
        'work_option2': work_option2,   # 근무옵션2
        'work_option3': work_option3,   # 근무옵션3
    }
    return db.Works.insert_one(work).inserted_id

def update_work(db, work_id, work_name, work_setting, work_option1, work_option2, work_option3):
    query = { 'work_id': work_id }
    values = {
        '$set': {
            'work_name': work_name,         # 근무명
            'work_setting': work_setting,   # 근무설정
          user_idk_option1': work_option1,   # 근무옵션1
            'work_option2': work_option2,   # 근무옵션2
            'work_option3': work_option3,   # 근무옵션3
        }
    }
    db.Works.update_one(query, values)

def find_work(db, work_id):
    query = { 'work_id': work_id }
    return db.Works.find_one(query)

def create_event(db, event_id, userid, event_title, event_type, work_id, tags, event_date, event_color, start_time, end_time):
    event = {
        'event_id': event_id,
        'userid': userid,
        'event_title': event_title,
        'event_type': int(event_type),
        'work_id': work_id,
        'tags': tags,
        'event_date': event_date,
        'event_color': event_color,
        'start_time': start_time,
        'end_time': end_time
    }
    return db.Events.insert_one(event).inserted_id

def insert_many_events(db, event_list):
    db.Events.insert_many(event_list)

def dbtest():
    clear_databases()
    dbtest1()
    dbtest2()
user_id
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
user_id
    update_user_on_userpage(db, 'test_id', '홍길동', 'test_pw', '2000-01-01', '2021-01-01', '2022-06-30', '병장', '1중대', '2소대', '3분대', '군사과학기술병', [], [])
    test_user = find_user(db, 'test_id')
    print(test_user)

def dbtest2():
    client = MongoClient('mongodb://localhost:27017/')
    db = db_init(client)
    create_work(db, 1, '불침번', [{'start_time':'22:00', 'end_time':'24:00', 'num_workers':2}], 1, 1, 1)
    create_work(db, 2, '당직', [{'start_time':'09:00', 'end_time':'08:59', 'num_workers':1}], 2, 2, 2)
    test_work = find_work(db, 1)
    print(test_work)
    test_work = find_work(db, 2)
    print(test_work)

    update_work(db, 1, '불침번', [{'start_time':'24:00', 'end_time':'02:00', 'num_workers':2}], 3, 3, 3)
    test_work = find_work(db, 1)
    print(test_work)

def dbtest3():
    client = MongoClient('mongodb://localhost:27017/')
    db = db_init(client)
    colors = ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1']
    create_event(
        db = db,
        event_id = 1,
        userid = 1,
        event_title = '위병소 근무',
        event_type = EventType.Work,
        work_id = 1,
        tags = [{'tag_title': '위병소', 'tag_color': colors[0]}, {'tag_title': '주간', 'tag_color': colors[1]}],
        event_date = '2021-10-13',
        event_color = colors[2],
        start_time = '10:00',
        end_time = '12:00'
    )
    create_event(
        db = db,
        event_id = 2,
        userid = 2,
        event_title = '불침번 근무',
        event_type = EventType.Work,
        work_id = 2,
        tags = [{'tag_title': '불침번', 'tag_color': colors[3]}, {'tag_title': '야간', 'tag_color': colors[4]}],
        event_date = '2021-10-15',
        event_color = colors[5],
        start_time = '22:00',
        end_time = '24:00'
    )

def create_custom_db():
    clear_databases()
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    # insert Works
    create_work(
        db = db,
        work_id = 1,
        work_name = '불침번',
        work_setting = [
            {'start_time': '22:00', 'end_time': '24:00', 'num_workers': 2},
            {'start_time': '00:00', 'end_time': '02:00', 'num_workers': 2},
            {'start_time': '02:00', 'end_time': '03:30', 'num_workers': 2},
            {'start_time': '03:30', 'end_time': '05:00', 'num_workers': 2},
            {'start_time': '05:00', 'end_time': '06:30', 'num_workers': 2}
        ],
        work_option1 = int(WorkOptionType.Allowed),
        work_option2 = int(WorkOptionType.Allowed),
        work_option3 = int(WorkOptionType.Never)
    )
    create_work(
        db = db,
        work_id = 2,
        work_name = '당직',
        work_setting = [
            {'start_time': '09:00', 'end_time': '09:00', 'num_workers': 1}
        ],
        work_option1 = int(WorkOptionType.Never),
        wouser_idion2 = int(WorkOptionType.NotPreferred),
        user_idption3 = int(WorkOptionType.Never)
    )
    create_work(
        db = db,
        work_id = 3,
        work_name = '경계',
        work_setting = [
            {'start_time': '06:00', 'end_time': '08:00', 'num_workers': 2},
            {'start_time': '08:00', 'end_time': '10:00', 'num_workers': 2},
            {'start_time': '10:00', 'end_time': '12:00', 'num_workers': 2},
            {'start_time': '12:00', 'end_time': '14:00', 'num_workers': 2},
            {'start_time': '14:00', 'end_time': '16:00', 'num_workers': 2},
            {'start_time': '16:00', 'end_time': '18:00', 'num_workers': 2},
            {'start_time': '18:00', 'end_time': '20:00', 'num_workers': 2},
            {'start_time': '20:00', 'end_time': '22:00', 'num_workers': 2}
        ],
        work_option1 = int(WorkOptionType.Allowed),
        work_option2 = int(WorkOptionType.Allowed),
        work_option3 = int(WorkOptionType.NotPreferred)
    )
    # insert Users
    name_list = [
        '도한수', '임본창', '한혜환', '최성우', '이대헌',
        '전도현', '정태현', '박현빈', '전남준', '탁승욱',
        '장영철', '봉영재', '오영근', '백우주', '김창환',
        '노지혁', '고진우', '하동석', '윤정환', '이대웅',
        '허광준', '유희준', '윤우일', '임유성', '안정훈',
        '서경수', '백종철', '임재성', '박준영', '남혜훈',
        '오성환', '허용태', '하승식', '서도환', '배병곤',
        '손명우', '안영원', '장승남', '조경호', '권진욱',
        '류정철user_id영',user_id, '안동현', '오동준',
        '장경민', '유시욱', '정민훈', '고진철', '정한길'
    ] # created by random generator
    position_list = [
        '소총수', '통신병', '의무병', '취사병', '운전병',
        '행정병', 'D.P', '정훈병'
    ]
    for i in range(50):
        # userid = 'uid' + str(f'{i:04d}')
        userid = str(i)
        name = name_list[i]
        password = 'pwd' + str(f'{i:04d}')
        birth_date = int_to_date(random.randint(date_to_int('1992-01-01'), date_to_int('2001-12-31')))
        en_date = int_to_date(random.randint(date_to_int('2020-05-01'), date_to_int('2021-10-01')))
        en_date_int = date_to_int(en_date)
        today_int = date_to_int('2021-10-13')
        diff = today_int - en_date_int
        de_date = int_to_date(en_date_int + 546)
        now_class = ''
        if diff < 60:
            now_class = '이병'
        elif diff < 240:
            now_class = '일병'
        elif diff < 420:
            now_class = '상병'
        else:
            now_class = '병장'
        unit_company = str(random.randint(1, 2)) + '중대'
        unit_platoon = str(random.randint(1, 3)) + '소대'
        unit_squad = str(random.randint(1, 3)) + '분대'
        position = random.choice(position_list)
        if i < 18:
            work = 1
        elif i < 26:
            work = 2
        else:
            work = 3
        create_user(
            db = db,
            userid = userid,
            name = name,
            password = password,
            birth_date = birth_date,
            en_date = en_date,
            de_date = de_date,
            now_class = now_class,
            unit_company = unit_company,
            unit_platuser_idunit_platoon,
            unit_squad = unit_squad,
            position = position,
            work_list = [work],
            vacation = []
        )

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
    user_list = db.Users.find()
    user_dict = {}
    for u in user_list:
        user_dict[u['userid']] = {'day_worktime':0, 'night_worktime':0, 'free_worktime':0, 'fatigue':0, 'work':u['work_list'], 'work_day_list':[]}
    return user_dict

def main():
    create_custom_db()

if __name__ == '__main__':
    main()
