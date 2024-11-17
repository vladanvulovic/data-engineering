from pyspark.sql.functions import col


# Conditions for each event type
def registration_valid():
    return (col("event_data").getItem("user_id").isNotNull()) & \
        (col("event_data").getItem("country").isNotNull()) & \
        (col("event_data").getItem("device_os").isNotNull())


def session_valid():
    return col("event_data.user_id").isNotNull()


def match_valid():
    return ((col("event_data.home_goals").isNotNull() & col("event_data.away_goals").isNotNull()) | \
       (col("event_data.home_goals").isNull() & col("event_data.away_goals").isNull()))
