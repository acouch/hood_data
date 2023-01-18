from libs.fetch_carto_data import fetch_carto_data_by_date
from libs.fetch_carto_data import build_carto_url
from libs.insert_json_to_bigquery import insert_json_to_bq
from airflow.models import BaseOperator
import pendulum
import datetime

# Date should be YYYY-MM-DD format or now(), add(days=), subtract(days=) pendulum func.
def getdate(date):
  add_str = "add("
  now_str = "now()"
  sub_str = "subtract("
  format = "%Y-%m-%d"
  pformat = "YYYY-MM-D"
  now = pendulum.now()

  # Checks for either add or sub format
  # todo: get regex value for period and pass instead of just days.
  if (date.startswith(add_str, 0, len(add_str)) or date.startswith(sub_str, 0, len(sub_str))) and (date[len(add_str):len(date)-3] == "days" or date[len(sub_str):len(date)-3] == "days"):
    n = int(date[len(date)-2:len(date)-1])
    # add(days=N) format
    if date.startswith(add_str, 0, len(add_str)):
      try:
        newDate = now.add(days=n).format(pformat)
        return newDate
      except ValueError:
        return False
    # subtract(days=N) format
    elif date.startswith(sub_str, 0, len(sub_str)):
      try:
        newDate = now.subtract(days=n).format(pformat)
        return newDate
      except ValueError:
        return False
  # now() format
  elif date.startswith(now_str, 0, len(now_str)):
    try:
      newDate = now.strftime(format)
      return newDate
    except ValueError:
      return False
  # YYYY-MM-DD format
  try:
    # Formats date in YYYY-MM-DD format
    newDate = str(datetime.datetime.strptime(date, format))[0:10]
    # Tests if correct format
    if (newDate == date):
      return date
    return False
  except ValueError:
    return False

class CartoToWarehouseOperator(BaseOperator):

    def __init__(
        self,
        warehouse_dataset,
        warehouse_table,
        carto_url,
        carto_table,
        carto_fields,
        carto_date_field,
        carto_start_date,
        carto_end_date,
        **kwargs,
    ) -> None:
        """An operator that fetches data from a carto instance and saves it to
            the warehouse.
        Args:
            warehouse_dataset (str): BQ dataset where the data will be saved.
            warehouse_table (str): BQ table where the data will be saved.
            carto_url (str): URL for Carto API.
            carto_table (str): Table to query from Carto.
            carto_fields (array): Fields to retrieve and store from Carto.
            carto_date_field (str): Date field to filter.
            start_date (str): YYYY-MM-DD date format OR 1 or 3 pendulum functions (now, add, subtract)
            end_date (str): YYYY-MM-DD date format OR 1 or 3 pendulum functions (now, add, subtract)
        """
        self.warehouse_dataset = warehouse_dataset
        self.warehouse_table = warehouse_table
        self.carto_url = carto_url
        self.carto_table = carto_table
        self.carto_fields = carto_fields
        self.carto_date_field = carto_date_field
        self.carto_start_date = carto_start_date
        self.carto_end_date = carto_end_date
        super().__init__(**kwargs)

    def execute(self, context):
        self.carto_start_date = getdate(self.carto_start_date)
        self.carto_end_date = getdate(self.carto_end_date)
        import logging
        LOGGER = logging.getLogger("airflow.task")
        url = build_carto_url(self.carto_url, self.carto_table, self.carto_fields, self.carto_date_field, self.carto_start_date, self.carto_end_date)
        LOGGER.info(f"Requesting carto data from {url}")
        data = fetch_carto_data_by_date(url)
        LOGGER.info("Requesting carto data received")
        if data.len:
          # todo: write to bucket
          LOGGER.info(f"Writing to bucket {self.warehouse_dataset} and table {self.warehouse_table}")
          return insert_json_to_bq(data, self.warehouse_dataset, self.warehouse_table)
        else:
          LOGGER.info("No data received from carto")
