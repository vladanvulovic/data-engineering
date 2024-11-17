from app.models import get_session_stats, get_best_player


def set_session_data(date, response):
    session_stats = get_session_stats(date)
    if session_stats:
        response["active_users"] = session_stats[0]["daily_active_users"]
        response["number_of_sessions"] = session_stats[0]["total_sessions"]
        if response["active_users"]:
            response["avg_sessions_for_users"] = round(float(response["number_of_sessions"]) / response["active_users"], 2)


def set_match_data(date, response):
    player = []
    best_player = get_best_player(date)
    if best_player:
        for row in best_player:
            player.append(row["user_id"])

    response["user_with_most_points"] = player


def get_game_stats(date=None):
    response = {
        "active_users": None,
        "number_of_sessions": None,
        "avg_sessions_for_users": None,
        "user_with_most_points": None
    }

    set_session_data(date, response)
    set_match_data(date, response)

    return response
