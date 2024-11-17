from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from constants import EVENT_TYPE_REGISTRATION, EVENT_TYPE_SESSION_PING, EVENT_TYPE_MATCH
from schemas import event_schema, timezones_schema
from processing.process_matches import process_matches
from processing.process_registrations import process_registrations
from processing.process_sessions import process_sessions
from event_validator import registration_valid, session_valid, match_valid
import sys
print(sys.path)

# Init SparkSession
spark = SparkSession.builder \
    .appName("JSONL Processing Pipeline") \
    .config("spark.jars", "/job/lib/postgresql-42.5.6.jar") \
    .getOrCreate()

# Load JSONL File
input_file = "/job/data/events.jsonl" #"../tests/events_test.jsonl"
df = spark.read.schema(event_schema).json(input_file, multiLine=False)

def filter_by_event_type(df, type):
    return df.filter(col("event_type") == type)


def clean_events(df, condition):
    filtered = df.filter(condition)
    return filtered.dropDuplicates(["event_id"]) # TODO Use common sense to discard other events that don’t make any sense

# process registration events
registration_df = filter_by_event_type(df, EVENT_TYPE_REGISTRATION)
registration_cleaned_df = clean_events(registration_df, registration_valid())
# Step 4: Load Timezones Data
timezones_file = "/job/data/timezones.jsonl"
timezones_df = spark.read.schema(timezones_schema).json(timezones_file, multiLine=False)
process_registrations(registration_cleaned_df, timezones_df)

# process session events
session_df = filter_by_event_type(df, EVENT_TYPE_SESSION_PING)
session_cleaned_df = clean_events(session_df, session_valid())
process_sessions(session_cleaned_df)

# process match events
match_df = filter_by_event_type(df, EVENT_TYPE_MATCH)
match_cleaned_df = clean_events(match_df, match_valid())
process_matches(match_cleaned_df)

# Stop the SparkSession
spark.stop()
