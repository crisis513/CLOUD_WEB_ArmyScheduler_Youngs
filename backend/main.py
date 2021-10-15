from pymongo import MongoClient
import random
import datetime
from typing import Dict, List
from enum import IntEnum

class Date(object):
    def __init__(self, date: int, isHoliday: bool):
        self.date = date
        self.date_string = int_to_date(date)
        self.isHoliday = isHoliday
    
    @classmethod
    def from_dict(cls, dict_item: Dict):
        return cls(
            date = dict_item['date'],
            isHoliday = dict_item['isHoliday']
        )
    
    def asdict(self):
        return {
            'date': self.date,
            'date_string': self.date_string,
            'isHoliday': self.isHoliday
        }

class Vacation(object):
    def __init__(self, start_date: str, end_date: str, description: str):
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
    
    @classmethod
    def from_dict(cls, dict_item: Dict):
        return cls(
            start_date = dict_item['start_date'],
            end_date = dict_item['end_date'],
            description = dict_item['description']
        )

    def asdict(self):
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'description': self.description
        }

class WorkTime(object):
    def __init__(self, day_worktime: int, night_worktime: int, free_worktime: int):
        self.day_worktime = day_worktime
        self.night_worktime = night_worktime
        self.free_worktime = free_worktime
    
    @classmethod
    def from_dict(cls, dict_item: Dict):
        return cls(
            day_worktime = dict_item['day_worktime'],
            night_worktime = dict_item['night_worktime'],
            free_worktime = dict_item['free_worktime']
        )

    def asdict(self):
        return {
            'day_worktime': self.day_worktime,
            'night_worktime': self.night_worktime,
            'free_worktime': self.free_worktime
        }

class WorkOptionType(IntEnum):
    Never = 0
    NotPreferred = 1
    Allowed = 2

class WorkSetting(object):
    def __init__(self, start_time: str, end_time: str, num_workers: int):
        self.start_time = start_time
        self.end_time = end_time
        self.num_workers = num_workers

    @classmethod
    def from_dict(cls, dict_item: Dict):
        return cls(
            start_time = dict_item['start_time'],
            end_time = dict_item['end_time'],
            num_workers = dict_item['num_workers']
        )

    def asdict(self):
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'num_workers': self.num_workers
        }

class Works(object):
    def __init__(
        self,
        work_id: int,
        work_name: str,
        worker_list: List[str],
        work_setting: List[WorkSetting],
        work_option1: WorkOptionType,
        work_option2: WorkOptionType,
        work_option3: WorkOptionType
    ):
        self.work_id = work_id
        self.work_name = work_name
        self.worker_list = worker_list
        self.work_setting = work_setting
        self.work_option1 = work_option1
        self.work_option2 = work_option2
        self.work_option3 = work_option3

    @classmethod
    def from_dict(cls, dict_item: Dict):
        return cls(
            work_id = dict_item['work_id'],
            work_name = dict_item['work_name'],
            worker_list = dict_item['worker_list'],
            work_setting = [WorkSetting.from_dict(ws) for ws in dict_item['work_setting']],
            work_option1 = WorkOptionType(dict_item['work_option1']),
            work_option2 = WorkOptionType(dict_item['work_option1']),
            work_option3 = WorkOptionType(dict_item['work_option1'])
        )

    def asdict(self):
        return {
            'work_id': self.work_id,
            'work_name': self.work_name,
            'worker_list': self.worker_list,
            'work_setting': [ws.asdict() for ws in self.work_setting],
            'work_option1': int(self.work_option1),
            'work_option2': int(self.work_option2),
            'work_option3': int(self.work_option3)
        }

class Users(object):
    def __init__(
        self,
        user_id: str,
        name: str,
        password: str,
        birth_date: str,
        en_date: str,
        de_date: str,
        now_class: str,
        unit_company: str,
        unit_platoon: str,
        unit_squad: str,
        position: str,
        work_list: List[int],
        vacation: List[Vacation],
        total_worked_time: WorkTime,
        this_month_worked_time: WorkTime,
        this_month_work_time_left: WorkTime,
        prev_month_worked_time: WorkTime,
        prev_day_worktime: int,
        prev_night_worktime: int,
        prev_free_worktime: int,
        new_day_worktime: int,
        new_night_worktime: int,
        new_free_worktime: int
    ):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.birth_date = birth_date
        self.en_date = en_date
        self.de_date = de_date
        self.now_class = now_class
        self.unit_company = unit_company
        self.unit_platoon = unit_platoon
        self.unit_squad = unit_squad
        self.position = position
        self.work_list = work_list
        self.vacation = vacation
        self.total_worked_time = total_worked_time
        self.this_month_worked_time = this_month_worked_time
        self.this_month_work_time_left = this_month_work_time_left
        self.prev_month_worked_time = prev_month_worked_time
        self.prev_day_worktime = prev_day_worktime
        self.prev_night_worktime = prev_night_worktime
        self.prev_free_worktime = prev_free_worktime
        self.new_day_worktime = new_day_worktime
        self.new_night_worktime = new_night_worktime
        self.new_free_worktime = new_free_worktime
        self.fatigue: int = 0
        self.last_work_day: int = -1

    @classmethod
    def from_dict(cls, dict_item):
        return cls(
            user_id = dict_item['user_id'],
            name = dict_item['name'],
            password = dict_item['password'],
            birth_date = dict_item['birth_date'],
            en_date = dict_item['en_date'],
            de_date = dict_item['de_date'],
            now_class = dict_item['now_class'],
            unit_company = dict_item['unit_company'],
            unit_platoon = dict_item['unit_platoon'],
            unit_squad = dict_item['unit_squad'],
            position = dict_item['position'],
            work_list = dict_item['work_list'],
            vacation = [Vacation.from_dict(v) for v in dict_item['vacation']],
            total_worked_time = WorkTime.from_dict(dict_item['total_worked_time']),
            this_month_worked_time = WorkTime.from_dict(dict_item['this_month_worked_time']),
            this_month_work_time_left = WorkTime.from_dict(dict_item['this_month_work_time_left']),
            prev_month_worked_time = WorkTime.from_dict(dict_item['prev_month_worked_time']),
            prev_day_worktime = dict_item['prev_day_worktime'],
            prev_night_worktime = dict_item['prev_night_worktime'],
            prev_free_worktime = dict_item['prev_free_worktime'],
            new_day_worktime = dict_item['new_day_worktime'],
            new_night_worktime = dict_item['new_night_worktime'],
            new_free_worktime = dict_item['new_free_worktime']
        )
    
    def asdict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'password': self.password,
            'birth_date': self.birth_date,
            'en_date': self.en_date,
            'de_date': self.de_date,
            'now_class': self.now_class,
            'unit_company': self.unit_company,
            'unit_platoon': self.unit_platoon,
            'unit_squad': self.unit_squad,
            'position': self.position,
            'work_list': self.work_list,
            'vacation': [v.asdict() for v in self.vacation],
            'total_worked_time': self.total_worked_time.asdict(),
            'this_month_worked_time': self.this_month_worked_time.asdict(),
            'this_month_work_time_left': self.this_month_work_time_left.asdict(),
            'prev_month_worked_time': self.prev_month_worked_time.asdict(),
            'prev_day_worktime': self.prev_day_worktime,
            'prev_night_worktime': self.prev_night_worktime,
            'prev_free_worktime': self.prev_free_worktime,
            'new_day_worktime': self.new_day_worktime,
            'new_night_worktime': self.new_night_worktime,
            'new_free_worktime': self.new_free_worktime
        }

class Tags(object):
    def __init__(self, tag_title: str, tag_color: str):
        self.tag_title = tag_title
        self.tag_color = tag_color
    
    @classmethod
    def from_dict(cls, dict_item: Dict):
        return cls(
            tag_title = dict_item['tag_title'],
            tag_color = dict_item['tag_color']
        )
    
    def asdict(self):
        return {
            'tag_title': self.tag_title,
            'tag_color': self.tag_color
        }

class EventType(IntEnum):
    Work = 0    # 근무
    Troop = 1   # 부대 일정 (훈련 등)
    Custom = 2  # 유저 개인 일정

class Events(object):
    def __init__(
        self,
        event_id: int,
        user_id: List[str],
        event_title: str,
        event_type: EventType,
        work_id: int,
        tags: List[Tags],
        event_color: str,
        event_start_date: Date,
        event_start_time: str,
        event_end_date: Date,
        event_end_time: str
    ):
        self.event_id = event_id
        self.user_id = user_id
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
    def from_dict(cls, dict_item: Dict):
        return cls(
            event_id = dict_item['event_id'],
            user_id = dict_item['user_id'],
            event_title = dict_item['event_title'],
            event_type = EventType(dict_item['event_type']),
            work_id = dict_item['work_id'],
            tags = [Tags.from_dict(t) for t in dict_item['tags']],
            event_color = dict_item['event_color'],
            event_start_date = Date.from_dict(dict_item['event_start_date']),
            event_start_time = dict_item['event_start_time'],
            event_end_date = Date.from_dict(dict_item['event_end_date']),
            event_end_time = dict_item['event_end_time']
        )

    @classmethod
    def from_scheduler(
        cls,
        event_id: int,
        start_date: Date,
        end_date: Date,
        tags: List[Tags],
        work_id: int,
        work_name: int,
        work_setting: WorkSetting
    ):
        return cls(
            event_id = event_id,
            user_id = [],
            event_title = work_name,
            event_type = EventType.Work,
            work_id = work_id,
            tags = tags,
            event_color = 'blue', # TODO: change this to work_color
            event_start_date = start_date,
            event_start_time = work_setting.start_time,
            event_end_date = end_date,
            event_end_time = work_setting.end_time
        )

    def asdict(self):
        return {
            'event_id': self.event_id,
            'user_id': self.user_id,
            'event_title': self.event_title,
            'event_type': int(self.event_type),
            'work_id': self.work_id,
            'tags': [tag.asdict() for tag in self.tags],
            'event_color': self.event_color,
            'event_start_date': self.event_start_date.asdict(),
            'event_start_time': self.event_start_time,
            'event_end_date': self.event_end_date.asdict(),
            'event_end_time': self.event_end_time
        }

def int_to_date(date: int) -> str:
    base_date = datetime.datetime.fromisoformat('1970-01-01')
    cur_date = base_date + datetime.timedelta(days=date)
    return datetime.datetime.strftime(cur_date, '%Y-%m-%d')

def date_to_int(date: str) -> int:
    base_date = datetime.datetime.fromisoformat('1970-01-01')
    cur_date = datetime.datetime.fromisoformat(date)
    diff = cur_date - base_date
    return diff.days

def db_init(client):
    db = client['army_scheduler_db']
    return db

def create_dates(db):
    date_list = []
    start_date = date_to_int('2021-01-01')
    end_date = date_to_int('2022-12-31')
    holiday_list = [
        '2021-01-01', '2021-02-11', '2021-02-12', '2021-02-13', '2021-03-01',
        '2021-05-05', '2021-05-19', '2021-06-06', '2021-08-15', '2021-08-16',
        '2021-09-20', '2021-09-21', '2021-09-22', '2021-10-03', '2021-10-04',
        '2021-10-09', '2021-10-11', '2021-12-25',
        '2022-01-01', '2022-01-31', '2022-02-01', '2022-02-02', '2022-03-01',
        '2022-03-09', '2022-05-05', '2022-05-08', '2022-06-01', '2022-06-06',
        '2022-08-15', '2022-09-09', '2022-09-10', '2022-09-11', '2022-09-12',
        '2022-10-03', '2022-12-25'
    ]
    for d in range(start_date, end_date + 1):
        date = int_to_date(d)
        query = {'date': d, 'isHoliday': False}
        if d % 7 in [2, 3]: # weekend
            query['isHoliday'] = True
        if date in holiday_list:
            query['isHoliday'] = True
        date_list.append(query)
    db.Dates.insert_many(date_list)

def update_date(db, date: int, isHoliday: bool):
    query = { 'date': date }
    value = {
        '$set': {
            'isHoliday': isHoliday
        }
    }
    db.Dates.update_one(query, value)

def create_user(db, user: Users):
    return db.Users.insert_one(user.asdict()).inserted_id

def find_user(db, uid):
    query = { 'user_id': uid }
    return db.Users.find_one(query)

def update_user_on_userpage(db, user_id, name, password, birth_date, en_date, de_date, now_class, unit_company, unit_platoon, unit_squad, position, work_list, vacation):
    query = { 'user_id': user_id }
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

def create_work(db, work: Works):
    return db.Works.insert_one(work.asdict()).inserted_id

def update_work(db, work_id, work_name, work_setting, work_option1, work_option2, work_option3):
    query = { 'work_id': work_id }
    values = {
        '$set': {
            'work_name': work_name,         # 근무명
            'work_setting': work_setting,   # 근무설정
            'work_option1': work_option1,   # 근무옵션1
            'work_option2': work_option2,   # 근무옵션2
            'work_option3': work_option3,   # 근무옵션3
        }
    }
    db.Works.update_one(query, values)

def find_work(db, work_id):
    query = { 'work_id': work_id }
    return db.Works.find_one(query)

def create_event(db, event_id, user_id, event_title, event_type, work_id, tags, event_date, event_color, start_time, end_time):
    event = {
        'event_id': event_id,
        'user_id': user_id,
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

def create_custom_db():
    clear_databases()
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    create_dates(db)
    print('Dates created')
    # insert Works
    w1 = Works(
        work_id = 1,
        work_name = '불침번',
        worker_list = [],
        work_setting = [
            WorkSetting(start_time='22:00', end_time='23:59', num_workers=2),
            WorkSetting(start_time='00:00', end_time='02:00', num_workers=2),
            WorkSetting(start_time='02:00', end_time='03:30', num_workers=2),
            WorkSetting(start_time='03:30', end_time='05:00', num_workers=2),
            WorkSetting(start_time='05:00', end_time='06:30', num_workers=2)
        ],
        work_option1 = WorkOptionType.Allowed,
        work_option2 = WorkOptionType.Allowed,
        work_option3 = WorkOptionType.Never
    )
    w2 = Works(
        work_id = 2,
        work_name = '당직',
        worker_list = [],
        work_setting = [
            WorkSetting(start_time='09:00', end_time='09:00', num_workers=1),
        ],
        work_option1 = WorkOptionType.Never,
        work_option2 = WorkOptionType.NotPreferred,
        work_option3 = WorkOptionType.Never
    )
    w3 = Works(
        work_id = 3,
        work_name = '경계',
        worker_list = [],
        work_setting = [
            WorkSetting(start_time='06:00', end_time='08:00', num_workers=2),
            WorkSetting(start_time='08:00', end_time='10:00', num_workers=2),
            WorkSetting(start_time='10:00', end_time='12:00', num_workers=2),
            WorkSetting(start_time='12:00', end_time='14:00', num_workers=2),
            WorkSetting(start_time='14:00', end_time='16:00', num_workers=2),
            WorkSetting(start_time='16:00', end_time='18:00', num_workers=2),
            WorkSetting(start_time='18:00', end_time='20:00', num_workers=2),
            WorkSetting(start_time='20:00', end_time='22:00', num_workers=2)
        ],
        work_option1 = WorkOptionType.Allowed,
        work_option2 = WorkOptionType.Allowed,
        work_option3 = WorkOptionType.NotPreferred
    )
    create_work(db, w1)
    create_work(db, w2)
    create_work(db, w3)
    print('Works created')
    # insert Users
    name_list = [
        '도한수', '임본창', '한혜환', '최성우', '이대헌', '전도현', '정태현', '박현빈', '전남준', '탁승욱',
        '장영철', '봉영재', '오영근', '백우주', '김창환', '노지혁', '고진우', '하동석', '윤정환', '이대웅',
        '허광준', '유희준', '윤우일', '임유성', '안정훈', '서경수', '백종철', '임재성', '박준영', '남혜훈',
        '오성환', '허용태', '하승식', '서도환', '배병곤', '손명우', '안영원', '장승남', '조경호', '권진욱',
        '류정철', '손규영', '손상민', '안동현', '오동준', '장경민', '유시욱', '정민훈', '고진철', '정한길'
    ]
    position_list = [
        '소총수', '통신병', '의무병', '취사병', '운전병', '행정병', 'D.P', '정훈병'
    ]
    for i in range(50):
        # user_id = 'uid' + str(f'{i:04d}')
        user_id = 'u'+str(i)
        name = name_list[i]
        password = 'pwd' + str(f'{i:04d}')
        birth_date = int_to_date(random.randint(date_to_int('1992-01-01'), date_to_int('2001-12-31')))
        en_date_int = random.randint(date_to_int('2020-05-01'), date_to_int('2021-10-01'))
        en_date = int_to_date(en_date_int)
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
        user = Users(
            user_id = user_id,
            name = name,
            password = password,
            birth_date = birth_date,
            en_date = en_date,
            de_date = de_date,
            now_class = now_class,
            unit_company = unit_company,
            unit_platoon = unit_platoon,
            unit_squad = unit_squad,
            position = position,
            work_list = [work],
            vacation = [],
            total_worked_time = WorkTime(0, 0, 0),
            this_month_worked_time = WorkTime(0, 0, 0),
            this_month_work_time_left = WorkTime(0, 0, 0),
            prev_month_worked_time = WorkTime(0, 0, 0),
            prev_day_worktime = 0,
            prev_night_worktime = 0,
            prev_free_worktime = 0,
            new_day_worktime = 0,
            new_night_worktime = 0,
            new_free_worktime = 0
        )
        create_user(db, user)
    print('Users created')

def clear_databases():
    client = MongoClient('mongodb://localhost:27017/') # for local test
    client.drop_database('army_scheduler_db')
    print(client.list_database_names())

def get_date_list(start_date: int, end_date: int) -> List[Date]:
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    dates = db.Dates.find({'date': {'$gte': start_date, '$lte': end_date}})
    date_list: List[Date] = []
    for d in dates:
        date_list.append(Date.from_dict(d))
    date_list.sort(key=lambda x: x.date)
    return date_list

def get_total_work_list() -> Dict[int, Works]:
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    works = db.Works.find()
    work_dict: Dict[int, Works] = {}
    for w in works:
        work_dict[w['work_id']] = Works.from_dict(w)
    return work_dict

def get_event_list_within(start_date: int, end_date: int) -> List[Events]:
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    events = db.Events.find({'event_start_date.date': {'$gte': start_date, '$lt': end_date}})
    events_list: List[Events] = []
    for e in events:
        events_list.append(Events.from_dict(e))
    return events_list

def get_total_user_list() -> Dict[str, Users]:
    client = MongoClient('mongodb://localhost:27017/') # for local test
    db = db_init(client)
    user_list = db.Users.find()
    user_dict: Dict[str, Users] = {}
    for u in user_list:
        user_dict[u['user_id']] = Users.from_dict(u)
    return user_dict

def main():
    create_custom_db()

if __name__ == '__main__':
    main()
