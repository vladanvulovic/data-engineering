from pyspark.sql.functions import col, from_utc_timestamp, from_unixtime, date_format

from job.db import write_to_postgres


def process_registrations(registration_df, timezones_df):
    registration_with_timezones = (registration_df.withColumn(
        "event_timestamp_ts",  # Convert BIGINT to TIMESTAMP
        from_unixtime(col("event_timestamp"))
    ).join(
        timezones_df,
        registration_df["event_data.country"] == timezones_df["country"],
        "left"
    ))
    registration_with_timezones = (registration_with_timezones.withColumn(
        "registration_date_local_timezone",
        date_format(from_utc_timestamp(col("event_timestamp_ts"), col("timezone")), "yyyy-MM-dd HH:mm:ss")
    ).select(
        col("event_data.user_id").alias("user_id"),
        col("event_data.country").alias("country"),
        col("registration_date_local_timezone"),
        col("event_data.device_os").alias("device")
    ))

    write_to_postgres(registration_with_timezones, "registration_data")