from airflow.models import BaseOperator

from plugins.services.postgres_admin_service import (
    PostgresAdminService
)


class CreateDatabaseOperator(BaseOperator):

    def __init__(
        self,
        postgres_conn_id,
        database_name = None,
        *args,
        **kwargsd
    ):

        super().__init__(*args, **kwargsd)

        self.postgres_conn_id = postgres_conn_id
        self.database_name = database_name



    def execute(self, context):

        service = PostgresAdminService(
            postgres_conn_id=self.postgres_conn_id
        )

        service.create_database(self.database_name)

            
    

 