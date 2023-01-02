from google.cloud import bigquery

def insert_json_to_bq(data, dataset, table):
    
    client = bigquery.Client()
    insert = client.insert_rows_json(f'{dataset}.{table}', data)
    return insert