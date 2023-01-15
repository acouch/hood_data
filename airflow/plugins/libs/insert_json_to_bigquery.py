import os
from google.cloud import bigquery
import sys

def insert_json_to_bq(data, dataset, table):
    import logging
    LOGGER = logging.getLogger("airflow.task")

    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    client = bigquery.Client()
    errors = client.insert_rows_json(f'{project}.{dataset}.{table}', data)
    if errors == []:
        LOGGER.info("New rows have been added.")
        return True
    else:
        LOGGER.info("Encountered errors while inserting rows: {}".format(errors))
        return False
