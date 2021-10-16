def user_helper(user) -> dict:
    return {
        "name": user['name'],
        "user_id": user['user_id'],
        "password": user['password'],
        "email": user['email'],
        "is_admin": user['is_admin'],
        "en_date": user['en_date'],
        "de_date": user['de_date'],
        "now_class": user['now_class'],
        "unit_company": user['unit_company'],
        "unit_platoon": user['unit_platoon'],
        "unit_squad": user['unit_squad'],
        "position": user['position'],
        "work_list": user['work_list'],
        "vacation": user['vacation'],
        "total_worked_time": user['total_worked_time'],
        "this_month_worked_time": user['this_month_worked_time'],
        "this_month_work_time_left": user['this_month_work_time_left'],
        "prev_month_worked_time": user['prev_month_worked_time'],
        "prev_day_worktime": user['prev_day_worktime'],
        "prev_night_worktime": user['prev_night_worktime'],
        "prev_free_worktime": user['prev_free_worktime'],
        "new_day_worktime": user['new_day_worktime'],
        "new_night_worktime": user['new_night_worktime'],
        "new_free_worktime": user['new_free_worktime'],
    }

def work_helper(work) -> dict:
    return {
        "work_id": work['work_id'],
        "work_name": work['work_name'],
        "worker_list": work['worker_list'],
        "work_setting": work['work_setting'],
        "work_option1": work['work_option1'],
        "work_option2": work['work_option2'],
        "work_option3": work['work_option3'],
    }

def event_helper(event) -> dict:
    return {
        "event_id": event['event_id'],
        "user_id": event['user_id'],
        "event_title": event['event_title'],
        "event_type": event['event_type'],
        "work_id": event['work_id'],
        "tags": event['tags'],
        "event_color": event['event_color'],
        "event_start_date": event['event_start_date'],
        "event_start_time": event['event_start_time'],
        "event_end_date": event['event_end_date'],
        "event_end_time": event['event_end_time'],
    }

def admin_helper(admin) -> dict:
    return {
        "id": str(admin['_id']),
        "fullname": admin['fullname'],
        "email": admin['email'],
    }
