from google.cloud import bigquery

def insert_json_to_bq(data, dataset, table):
    
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset)
    table_ref = dataset_ref.table(table)
    table = client.get_table(table_ref)
    insert = client.insert_rows_json(table, data)
    return insert