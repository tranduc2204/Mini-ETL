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

    def create_database(self, database_name):
        
        self.hook.crseate_database(database_name)

    def create_schema(self, schema_name):
        # self.hook.create_database()
        self.hook.create_schema(schema_name) # para is info schema name

    
    # def setup_silver_layer(self):

    #     self.hook.create_schema("silver")

    # def setup_gold_layer(self):

    #     self.hook.create_schema("gold")

    def create_table(self, schema_name, table_name, columns):

        self.hook.create_table(schema_name, table_name, columns) 