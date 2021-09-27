from pymongo import MongoClient

def db_init(client):
    db = client['army_scheduler_db'] # DB
    Users = db['Users']              # 유저 정보
    Works = db['Works']              # 근무 정보
    Events = db['Events']            # 유저에게 할당되는 이벤트(근무 등)

def main():
    client = MongoClient('mongodb://crlee:myPassword@20.194.38.223:3306/army_scheduler_db')
    db_init(client)

if __name__ == '__main__':
    main()

