from libs.fetch_carto_data import fetch_carto_data_by_date
from libs.insert_json_to_bigquery import insert_json_to_bq
from airflow.models import BaseOperator

class CartoToWarehouseOperator(BaseOperator):

    template_fields = ("bucket",)

    def __init__(
        self,
        warehouse_dataset,
        warehouse_table,
        carto_url,
        carto_table,
        carto_fields,
        carto_date_field,
        start_date,
        end_date,
        **kwargs,
    ):
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
        self.start_date = start_date
        self.end_date = end_date
        super().__init__(**kwargs)

    def execute(self, **kwargs):
        data = fetch_carto_data_by_date(self.carto_url, self.carto_table, self.carto_fields, self.carto_date_field, self.start_date, self.end_date)
        # todo: write to bucket
        insert_json_to_bq(data, self.warehouse_dataset, self.warehouse_table)
        return self.extract.save_to_gcs(fs, self.bucket)