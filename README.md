# data-engineering

Create a Spark job that will read the data from the input file and write the output.
Job should clean the data (validate all the rules) and calculate needed metrics. 
(bonus - without the column “type”?)
It should output the results in a DB that can be easily queried.

API should be able to expose an endpoint (method) to get stats for the given user and output some response in a following format:
```json
{
    "user_id": "123456",
    "country": "US",
    "days_since_last_login": 1,
    "registration_date_local_timezone": "2024-10-09 11:27:35",
    "number_of_sessions": 2,
    "time_spent_in_game": 780,
    "total_points_won_home": 3,
    "total_points_won_away": 0,
    "percentage_time_spent_in_match": 0.23
}
```
## Part 1 - Data processing job
We will use Spark to process the data (can be easily scaled if needed) - that project is inside `job` directory.
Idea is to split events into three groups (by event type- registration, session and game) because each group has its own validation rules and different ways to aggregate.
We will store the results in a database (Postgres?) and expose an API to query the results.

## Data Model
We will use the following DB schema for aggregations:
```
CREATE TABLE registration_data (
                                   user_id UUID PRIMARY KEY,
                                   country VARCHAR(50),
                                   registration_date_local_timezone TIMESTAMP,
                                   device VARCHAR(50)
);

CREATE TABLE session_data (
                              user_id UUID,
                              date DATE,
                              session_count INT,
                              time_spent_in_game BIGINT,
                              PRIMARY KEY (user_id, date)
);

CREATE TABLE match_data (
                            user_id UUID,
                            date DATE,
                            total_duration BIGINT,
                            total_points_home INT,
                            total_points_away INT,
                            PRIMARY KEY (user_id, date)
);
```
It's daily aggregated data for each user where we can easily query the results. 
Also, we can run data processing in a batch mode incrementally.

## Part 2 - API
On top of aggregations, we will create a API to query the results using SQL queries.
We will use Flask application to expose the API - that part is inside `api` directory.

For querying part - we will split the query into parts - we could maybe create one big query to fetch it all in at once but let's split it first.

## How to run
1. use `docker-compose up` to start the services
2. Wait ~10s and API will be available at `http://localhost:5000/api/user-stats?user_id=52d65a1b-8012-934e-001b-19e6ba3cdc0e&date=2024-10-09` and `http://localhost:5000/api/game-stats`

# TODO move db_config, set event files
