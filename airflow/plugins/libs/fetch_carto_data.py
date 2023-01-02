import requests
import json
import sys

def fetch_carto_data_by_date(cartol_url, fields, table, date_field, start_date, end_date):
    where_clause = f"{date_field} >= '{start_date}' AND {date_field} < '{end_date}'"
    string_fields = ','.join(fields)
    url = f"{cartol_url}?filename={table}&format=json&q=SELECT {string_fields} FROM {table} WHERE {where_clause}"
    response_API = requests.get(url)
    if response_API.status_code == 200:
        return json.loads(response_API.text)
    else:
        print(f"Carto request returned with status: {response_API.status_code}")
        return sys.exit(1)

