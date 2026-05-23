from airflow.models import BaseOperator

from plugins.services.postgres_admin_service import (
    PostgresAdminService
)


class CreateSchemaOperator(BaseOperator):

    def __init__(
        self,
        postgres_conn_id,
        schema_name = None,
        *args,
        **kwargsd
    ):

        super().__init__(*args, **kwargsd)

        self.postgres_conn_id = postgres_conn_id

        self.schema_name = schema_name



    def execute_database(self, context):

        service = PostgresAdminService(
            postgres_conn_id=self.postgres_conn_id
        )

        service.create_database(self.database_name)

            
    

    def create_schema (self, context):

        service = PostgresAdminService(
            postgres_conn_id=self.postgres_conn_id
        )

        service.create_schema(self.schema_name)

