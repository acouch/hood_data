import requests
import json
import sys

def build_carto_url(cartol_url, table, fields, date_field, start_date, end_date):
    string_fields = ','.join(fields)
    where_clause = f"{date_field} >= '{start_date}' AND {date_field} < '{end_date}'"
    return f"{cartol_url}?filename={table}&format=json&q=SELECT {string_fields} FROM {table} WHERE {where_clause}"
    
def fetch_carto_data_by_date(url):
    response_API = requests.get(url)
    if response_API.status_code == 200:
        return json.loads(response_API.text)["rows"]
    else:
        print(f"Carto request to {url} returned with status: {response_API.status_code}")
        return sys.exit(1)
