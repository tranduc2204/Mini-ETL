from plugins.hooks.postgres_admin_hook import (
    PostgresAdminHook
)


class PostgresAdminService:

    def __init__(
        self,
        postgres_conn_id
    ):

        self.hook = PostgresAdminHook(
            postgres_conn_id=postgres_conn_id
        )

    def setup_bronze_layer(self):

        self.hook.create_schema("bronze")

    def setup_silver_layer(self):

        self.hook.create_schema("silver")

    def setup_gold_layer(self):

        self.hook.create_schema("gold")