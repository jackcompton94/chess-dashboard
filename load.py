from datetime import datetime, time
import os
from google.cloud import bigquery
import table

# Table name date config
month = datetime.today()
monthString = str(month.month)

if int(monthString) < 10:
    monthString = "0" + monthString

# Configures source_file name based on current date
file_path = "/Users/jackcompton/PycharmProjects/chessDashboard/csvs/" + month.strftime("%m_%Y") + "_games.csv"

# Authorize BigQuery
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= '/Users/jackcompton/PycharmProjects/chessDashboard/peak-vortex-376919-de9924963ab6.json'

# Creates a BigQuery client object and initializes the job
client = bigquery.Client()
job_config = bigquery.LoadJobConfig(
    source_format = bigquery.SourceFormat.CSV,
    skip_leading_rows = 1,
    autodetect = True
)

# Sets the id of the table - "peak-vortex-376919.chess_dashboard" is the BigQuery dataset name
table_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_games"

# Sets the schema for table
table_schema = [
    bigquery.SchemaField("game_id", "INTEGER"),
    bigquery.SchemaField("white", "STRING"),
    bigquery.SchemaField("white_rating", "INTEGER"),
    bigquery.SchemaField("white_result", "STRING"),
    bigquery.SchemaField("black", "STRING"),
    bigquery.SchemaField("black_rating", "INTEGER"),
    bigquery.SchemaField("black_result", "STRING")
]

# Checks if table exists and deletes
if table.if_table_exists(client, table_id):
    delete_query = f"DELETE FROM {table_id} WHERE True"
    client.query(delete_query)

    # Opening local file to fill table
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    print(job.result())

    table = client.get_table(table_id)
    print("Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
        )
    )
else:
    # If doesn't exist - creates a table object
    table = bigquery.Table(table_id, schema=table_schema)
    table = client.create_table(table)

    # Opening local file to fill table
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    print(job.result())

    table = client.get_table(table_id)
    print("Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
        )
    )
