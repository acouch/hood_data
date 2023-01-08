import os
from google.cloud import bigquery
import sys

def insert_json_to_bq(data, dataset, table):

    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    client = bigquery.Client()
    insert = client.insert_rows_json(f'{project}.{dataset}.{table}', data)
    return insert