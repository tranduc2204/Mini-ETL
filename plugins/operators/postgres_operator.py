from airflow.models import BaseOperator

from plugins.services.postgres_admin_service import (
    PostgresAdminService
)


class CreateSchemaOperator(BaseOperator):

    def __init__(
        self,
        postgres_conn_id,
        layer_name,
        *args,
        **kwargs
    ):

        super().__init__(*args, **kwargs)

        self.postgres_conn_id = postgres_conn_id
        self.layer_name = layer_name

    def execute(self, context):

        service = PostgresAdminService(
            postgres_conn_id=self.postgres_conn_id
        )

        if self.layer_name == "bronze":
            service.setup_bronze_layer()

        elif self.layer_name == "silver":
            service.setup_silver_layer()

        elif self.layer_name == "gold":
            service.setup_gold_layer()

        self.log.info(
            f"{self.layer_name} schema created"
        )