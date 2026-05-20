import re
from airflow.providers.postgres.hooks.postgres import PostgresHook

class PostgresAdminHook(PostgresHook):

    def validate_name(self, name):

        if not re.match(r"^[a-zA-Z0-9_]+$", name):
            raise ValueError(
                f"Invalid name: {name}"
            )

    def create_database(self, database_name):

        self.validate_name(database_name)

        conn = self.get_conn()

        conn.autocommit = True

        cursor = conn.cursor()

        cursor.execute(
            f"""
            CREATE DATABASE {database_name};
            """
        )

        cursor.close()
        conn.close()

    def create_schema(self, schema_name):

        self.validate_name(schema_name)

        sql = f"""
        CREATE SCHEMA IF NOT EXISTS {schema_name};
        """

        self.run(sql)










