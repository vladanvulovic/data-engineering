from pyspark.sql import Window
from pyspark.sql.functions import col, lag, when, count, min as spark_min, max as spark_max, from_unixtime, coalesce, \
    lit, sum as spark_sum

from job.db import write_to_postgres


def process_sessions(session_cleaned_df):
    # Step 6: Calculate Number of Sessions Using Windowing
    # Define a window partitioned by user_id and ordered by event_timestamp
    window_spec = Window.partitionBy(col("event_data.user_id")).orderBy(col("event_timestamp"))
    # Calculate time difference between consecutive events
    df_sessions = session_cleaned_df.withColumn("prev_timestamp", lag("event_timestamp").over(window_spec))
    df_sessions = df_sessions.withColumn("time_diff", (col("event_timestamp") - col("prev_timestamp")))
    # Identify session starts (time_diff > 60 seconds or first event)
    df_sessions = df_sessions.withColumn("is_new_session", \
                                         when(col("prev_timestamp").isNull(), 1).otherwise(
                                             when(col("time_diff") > 60, 1).otherwise(0)))
    # Calculate session IDs by cumulative sum of is_new_session
    df_sessions = df_sessions.withColumn("session_id", spark_sum("is_new_session").over(
        window_spec.rowsBetween(Window.unboundedPreceding, Window.currentRow)))

    session_aggregated = df_sessions.groupBy("event_data.user_id", "session_id").agg(
        spark_min("event_timestamp").alias("session_start"),
        spark_max("event_timestamp").alias("session_end")
    )

    session_aggregated = session_aggregated.withColumn(
        "session_duration",
        (col("session_end") - col("session_start"))
    )

    session_aggregated = session_aggregated.withColumn("date", from_unixtime(col("session_start")).cast("date"))  # Convert to TIMESTAMP and then to DATE

    df_session_counts = session_aggregated.groupBy("user_id", "date").agg(
        count("session_id").alias("session_count"),
        spark_sum(coalesce(col("session_duration"), lit(0))).alias("time_spent_in_game")
    )

    write_to_postgres(df_session_counts, "session_data")
