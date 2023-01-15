from libs.fetch_carto_data import fetch_carto_data_by_date
from libs.insert_json_to_bigquery import insert_json_to_bq
from airflow.models import BaseOperator
import pendulum

# Passes params to get dates using pendulum methods.
# Args:
#   operator (string): "now", "add", or "subtract"
#   operator_period (string): Any of the period values supported by pendulum
#   operator_value (int): Value to change the operator_period
#   format (string): Desired date format.  
def date_change(operator, operator_period = "days", operator_value = 1, format = "YYYY-MM-DD"):
  now = pendulum.now()
  if operator == "now":
    return now.format(format)
  elif operator == "add":
    date = now.add(**{operator_period:operator_value}).format(format)
    return date
  elif operator == "subtract":
    date = now.subtract(**{operator_period:operator_value}).format(format)
    return date
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
            carto_start_date (str): YYYY-MM-DD date format OR 1 or 3 pendulum functions (now, add, subtract)
            carto_end_date (str): YYYY-MM-DD date format OR 1 or 3 pendulum functions (now, add, subtract)
            start_date_operator (string): "now", "add", or "subtract" for start date
            start_date_operator_period (string): Any of the period values supported by pendulum for start date
            start_date_operator_value (int): Value to change the operator_period for start date
            end_date_operator (string): "now", "add", or "subtract" for end date
            end_operator_period (string): Any of the period values supported by pendulum for end date
            end_operator_value (int): Value to change the operator_period for end date
        """
        self.warehouse_dataset = warehouse_dataset
        self.warehouse_table = warehouse_table
        self.carto_url = carto_url
        self.carto_table = carto_table
        self.carto_fields = carto_fields
        self.carto_date_field = carto_date_field
        # Explicit start and end date or pendulum date add/subtract can be added.
        self.carto_start_date = None if 'carto_start_date' not in locals() else carto_start_date
        self.carto_end_date =  None if 'carto_end_date' not in locals() else carto_end_date
        self.end_date_operator = None if 'end_date_operator' not in locals() else end_date_operator
        self.end_date_operator_period = None if 'end_date_operator_period' not in locals() else end_date_operator_period
        self.end_date_operator_value = None if 'end_date_operator_value' not in locals() else end_date_operator_value
        self.start_date_operator = None if 'start_date_operator' not in locals() else start_date_operator
        self.start_date_operator_period = None if 'start_date_operator_period' not in locals() else start_date_operator_period
        self.start_date_operator_value = None if 'start_date_operator_value' not in locals() else start_date_operator_value
        super().__init__(**kwargs)

    def execute(self, context):
        if (self.start_date_operator):
            self.carto_start_date = date_change(self.start_date_operator, self.start_date_operator_period, self.start_date_operator_value)
        if (self.end_date_operator):
            self.carto_end_date = date_change(self.end_date_operator, self.end_date_operator_period, self.end_date_operator_value)
        if (self.carto_end_date is None or self.carto_end_date is None):
            SystemError("carto_start_date and carto_end_date or carto_[]_operator not specified")
        import logging
        LOGGER = logging.getLogger("airflow.task")
        LOGGER.info("Requesting carto data")
        data = fetch_carto_data_by_date(self.carto_url, self.carto_table, self.carto_fields, self.carto_date_field, self.carto_start_date, self.carto_end_date)
        LOGGER.info("Requesting carto data received")
        # todo: write to bucket
        LOGGER.info(f"Writing to bucket {self.warehouse_dataset} and table {self.warehouse_table}")
        return insert_json_to_bq(data, self.warehouse_dataset, self.warehouse_table)