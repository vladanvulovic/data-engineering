from pyspark.sql import Window
from pyspark.sql.functions import col, lag, when, from_unixtime, \
    lit, sum as spark_sum, date_format

from job.db import write_to_postgres

def process_matches(match_cleaned_df):
    window_spec = Window.partitionBy(col("event_data.match_id")).orderBy(col("event_timestamp"))
    match_intermediate = match_cleaned_df.withColumn(
        "duration",
        col("event_timestamp") - lag("event_timestamp").over(window_spec)
    ).filter(
        col("duration").isNotNull()  # Evict rows where duration is NULL
    ).withColumn(
        "result",
        when(col("event_data.home_goals_scored") > col("event_data.away_goals_scored"), lit(1))
        .when(col("event_data.home_goals_scored") < col("event_data.away_goals_scored"), lit(2))
        .otherwise(lit("x"))
    ).select(
        col("event_data.match_id").alias("match_id"),
        date_format(from_unixtime(col("event_timestamp")), "yyyy-MM-dd").alias("date"),
        col("event_data.home_user_id").alias("home_user"),
        col("event_data.away_user_id").alias("away_user"),
        "duration",
        "result"
    )

    # Step 2: Assign points to home and away users
    match_points = match_intermediate.withColumn(
        "home_points",
        when(col("result") == 1, lit(3)).when(col("result") == "x", lit(1)).otherwise(lit(0))
    ).withColumn(
        "away_points",
        when(col("result") == 2, lit(3)).when(col("result") == "x", lit(1)).otherwise(lit(0))
    )

    # Step 3: Flatten to user-level statistics
    home_stats = match_points.select(
        col("home_user").alias("user_id"),
        "date",
        "duration",
        col("home_points").alias("points_home"),
        lit(0).alias("points_away")
    )

    away_stats = match_points.select(
        col("away_user").alias("user_id"),
        "date",
        "duration",
        lit(0).alias("points_home"),
        col("away_points").alias("points_away")
    )

    user_match_stats = home_stats.union(away_stats)

    # Step 4: Aggregate results per user and date
    user_match_aggregated = user_match_stats.groupBy("user_id", "date").agg(
        spark_sum("duration").alias("total_duration"),
        spark_sum("points_home").alias("total_points_home"),
        spark_sum("points_away").alias("total_points_away")
    )
    write_to_postgres(user_match_aggregated, "match_data")
