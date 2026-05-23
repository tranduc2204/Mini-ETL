from ast import arg
from typing import List, Dict

from airflow.models import BaseOperator

from plugins.services.postgres_admin_service import (
    PostgresAdminService
)


class CreateTableOperator(BaseOperator):

    def __init__(
        self,
        postgres_conn_id,
        schema_name = None,
        table_name = None,
        columns: List[Dict] | None = None,
        *args,
        **kwargsd
    ):

        super().__init__(*args, **kwargsd)



        self.postgres_conn_id = postgres_conn_id

        self.schema_name = schema_name
        self.table_name = table_name
        self.columns = columns 
        



    def execute(self, context):

        service = PostgresAdminService(
            postgres_conn_id=self.postgres_conn_id
        )

        service.create_table(self.schema_name, self.table_name, self.columns)
        # service.create_table(
        #     "bronze",
        #     "orders_cdc_log",
        #     [
        #         {"name": "order_id", "type": "INT"},
        #         {"name": "changed_at", "type": "TIMESTAMP"},
        #         {"name": "operation", "type": "VARCHAR(10)"}
        #     ]
        # )