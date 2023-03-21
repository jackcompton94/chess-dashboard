from google.cloud import bigquery
import view
from config import config


def upload_to_bigquery():
    import table

    # Creates a BigQuery client object and initializes the job
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=False
    )

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
    if table.if_table_exists(client, config.table_id):
        delete_query = f"DELETE FROM {config.table_id} WHERE True"
        client.query(delete_query)

        load_table_from_csv(client, config.table_id, job_config)


    else:
        # If doesn't exist - creates a table object
        table = bigquery.Table(config.table_id, schema=table_schema)
        table = client.create_table(table)

        load_table_from_csv(client, config.table_id, job_config)

        # Initialize views
        view.initialize_views(client, config.month, config.table_id)


def load_table_from_csv(client, table_id, job_config):
    with open(config.file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)

    print(job.result())

    table = client.get_table(config.table_id)
    print("Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), config.table_id))

