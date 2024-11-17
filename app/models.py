import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "postgres",
    "port": 5432,
}

def get_registration_data(user_id):
    query = """
        SELECT country, registration_date_local_timezone
        FROM registration_data
        WHERE user_id = %s
    """
    params = [user_id]
    return execute_query(query, params)

def get_session_data(user_id, date=None):
    query = """
        SELECT date, session_count, time_spent_in_game
        FROM session_data
        WHERE user_id = %s
    """
    params = [user_id]
    if date:
        query += " AND date = %s"
        params.append(date)
    return execute_query(query, params)

def get_last_user_session_before_day(user_id, date):
    query = """
        SELECT *
            FROM session_data
            WHERE user_id = %s and date < %s
            ORDER BY date DESC
            LIMIT 1
    """
    params = [user_id, date]
    return execute_query(query, params)

def get_session_stats(date):
    query = """
        SELECT  
            COALESCE(COUNT(user_id), 0) AS daily_active_users, 
            COALESCE(SUM(session_count), 0) AS total_sessions
        FROM 
            session_data
        WHERE 
            session_count > 0 """
    params = []
    if date:
        query += " AND date = %s"
        params.append(date)
    return execute_query(query, params)

def get_best_player(date):
    query = """
        WITH user_points AS (
        SELECT 
            user_id,
            SUM(total_points_home + total_points_away) AS total_points
        FROM 
            match_data """
    params = []
    if date:
        query += " WHERE date = %s "
        params.append(date.strftime('%Y-%m-%d'))
    query += """
        GROUP BY user_id
        )
        SELECT user_id, total_points
        FROM 
            user_points
        WHERE 
            total_points = (SELECT MAX(total_points) FROM user_points)
        ORDER BY 
            user_id;"""
    return execute_query(query, params)

def get_match_data(user_id, date=None):
    query = """
        SELECT date, total_duration, total_points_home, total_points_away
        FROM match_data
        WHERE user_id = %s """
    params = [user_id]
    if date:
        query += " AND date = %s"
        params.append(date.strftime("%Y-%m-%d"))
    return execute_query(query, params)

def execute_query(query, params):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params)
        results = cur.fetchall()
        conn.close()
        return results
    except Exception as e:
        raise Exception(f"Database query failed: {e}")
