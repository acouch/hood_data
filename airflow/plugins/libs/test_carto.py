from libs.fetch_carto_data import fetch_carto_data_by_date

# todo: remove this file

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

fetch_carto_data_by_date(date_field, start_date, end_date)
