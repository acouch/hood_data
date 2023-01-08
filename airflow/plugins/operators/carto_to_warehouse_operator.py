from libs.fetch_carto_data import fetch_carto_data_by_date
#from libs.insert_json_to_bigquery import insert_json_to_bq
from airflow.models import BaseOperator

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
            carto_url (str):
            carto_table (str):
            carto_fields (array):
            carto_date_field (str):
            start_date (str):
            end_date (str):
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
        import logging
        LOGGER = logging.getLogger("airflow.task")
        LOGGER.info("Requesting carto data")
        data = fetch_carto_data_by_date(self.carto_url, self.carto_table, self.carto_fields, self.carto_date_field, self.carto_start_date, self.carto_end_date)
        LOGGER.info("Requesting carto data received")
        # todo: write to bucket
        LOGGER.info(f"Writing to bucket {self.warehouse_dataset} and table {self.warehouse_table}")
        return insert_json_to_bq(data, self.warehouse_dataset, self.warehouse_table)