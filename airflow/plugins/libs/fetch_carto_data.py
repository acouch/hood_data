import requests
import json
import sys

carto_url = "https://phl.carto.com/api/v2/sql"
table = "public_cases_fc"
fields = [
    "service_request_id",
    "subject",
    "status,status_notes",
    "service_name",
    "service_code",
    "agency_responsible",
    "service_notice",
    "requested_datetime",
    "updated_datetime",
    "expected_datetime",
    "closed_datetime",
    "address",
    "zipcode",
    "media_url",
    ]
date_field = "requested_datetime"
start_date = "2022-12-30"
end_date = "2023-01-01"

def fetch_carto_data(cartol_url, fields, table, where_clause):
    string_fields = ','.join(fields)
    url = f"{cartol_url}?filename={table}&format=json&q=SELECT {string_fields} FROM {table} WHERE {where_clause}"
    response_API = requests.get(url)
    if response_API.status_code == 200:
        return json.loads(response_API.text)
    else:
        print(f"Carto request returned with status: {response_API.status_code}")
        return sys.exit(1)

def fetch_carto_data_by_date(date_field, start_date, end_date):
    where_clause = f"{date_field} >= '{start_date}' AND {date_field} < '{end_date}'"
    data = fetch_carto_data(carto_url, fields, table, where_clause)
    return data

fetch_carto_data_by_date(date_field, start_date, end_date)
