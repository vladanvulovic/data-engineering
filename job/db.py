from pyspark.sql import DataFrame

def write_to_postgres(df: DataFrame, table_name: str):
    """
    Writes a Spark DataFrame to a PostgreSQL table.
    """
    df.write.jdbc(
        url=db_url,
        table=table_name,
        mode="overwrite",
        properties=db_properties
    )

# Database connection details
db_url = "jdbc:postgresql://postgres:5432/postgres"
db_properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

