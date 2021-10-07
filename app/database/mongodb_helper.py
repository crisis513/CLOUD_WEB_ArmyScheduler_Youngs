
def user_helper(user) -> dict:
    return {
        "name": user['name'],
        "userid": user['userid'],
        "password": user['password'],
        "en_date": user['en_date'],
        "de_date": user['de_date'],
        "now_class": user['now_class'],
        "unit_company": user['unit_company'],
        "unit_platoon": user['unit_platoon'],
        "unit_squad": user['unit_squad'],
        "position": user['position'],
        "work_list": user['work_list'],
        "vacation": user['vacation'],
        "total_work_time": user['total_work_time'],
        "this_mon_work_time": user['this_mon_work_time'],
        "prev_mon_work_time": user['prev_mon_work_time']

    }
