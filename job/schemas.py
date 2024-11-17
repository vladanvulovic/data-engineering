from pyspark.sql.types import StructType, StructField, IntegerType, StringType, LongType, MapType

event_schema = StructType([
    StructField("event_id", IntegerType(), True),
    StructField("event_type", StringType(), True),
    StructField("event_timestamp", LongType(), True),
    StructField("event_data", MapType(StringType(), StringType()), True)
])

timezones_schema = StructType([
    StructField("country", StringType(), True),
    StructField("timezone", StringType(), True)
])