from datetime import datetime
from app.models import get_registration_data, get_last_user_session_before_day, get_session_data, get_match_data


def set_registration_data(user_id, response):
    reg_data = get_registration_data(user_id)
    if not reg_data:
        return
    else:
        reg_data = reg_data[0]
        response["country"] = reg_data["country"]
        response["registration_date_local_timezone"] = reg_data["registration_date_local_timezone"]


def set_session_data(user_id, date, response):
    lookback_date = date if date else datetime.today().date() # we are looking back from the date if it is provided, otherwise we are looking back from now
    last_user_session = get_last_user_session_before_day(user_id, lookback_date)
    if last_user_session:
        last_user_session_date = last_user_session[0]["date"]
        response["days_since_last_login"] = (lookback_date - last_user_session_date).days
    session_data = get_session_data(user_id, date)
    total_session_count = 0
    total_time_spent_in_game = 0
    if session_data:
        for row in session_data:
            total_session_count += row["session_count"]
            total_time_spent_in_game += row["time_spent_in_game"]

    response["number_of_sessions"] = total_session_count
    response["time_spent_in_game"] = total_time_spent_in_game


def set_match_data(user_id, date, response):
    all_match_data = get_match_data(user_id, date)
    total_points_won_home = 0
    total_points_won_away = 0
    total_time_spent_in_match = 0
    if all_match_data:
        for row in all_match_data:
            total_points_won_home += row["total_points_home"]
            total_points_won_away += row["total_points_away"]
            total_time_spent_in_match += row["total_duration"]

    response["total_points_won_home"] = total_points_won_home
    response["total_points_won_away"] = total_points_won_away
    if response["time_spent_in_game"] == 0:
        response["percentage_time_spent_in_match"] = 0
    else:
        result = total_time_spent_in_match / response["time_spent_in_game"] * 100
        response["percentage_time_spent_in_match"] = round(result, 2)


def get_user_stats(user_id, date=None):

    response = {
        "country": None,
        "days_since_last_login": None,
        "registration_date_local_timezone": None,
        "number_of_sessions": None,
        "time_spent_in_game": None,
        "total_points_won_home": None,
        "total_points_won_away": None,
        "percentage_time_spent_in_match": None
    }

    set_registration_data(user_id, response)
    set_session_data(user_id, date, response)
    set_match_data(user_id, date, response)

    return response
