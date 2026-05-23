import re

from sqlalchemy import exists
from airflow.providers.postgres.hooks.postgres import PostgresHook

class PostgresAdminHook(PostgresHook):

    def validate_name(self, name):

        if not re.match(r"^[a-zA-Z0-9_]+$", name):
            raise ValueError(
                f"Invalid name: {name}"
            )

    def create_schema(self, schema_name):

        self.validate_name(schema_name)

        sql = f"""
            CREATE SCHEMA IF NOT EXISTS {schema_name};
        """

        self.run(sql)

   
    def create_database (self, database_name):

        self.validate_name(database_name)

        conn = self.get_conn()

        conn.autocommit = True

        cursor = conn.cursor()

        # check exists database
        cursor.execute(
            """
            SELECT 1 FROM pg_database WHERE datname = %s;
            """,
            (database_name,)
        )

        if cursor.fetchone():
            print (f"Database {database_name} already exists")
        else:
            cursor.execute(
                f"""
                CREATE DATABASE {database_name};
                """
            )

        cursor.close()
        conn.close()


    def create_table (self, schema_name, table_name, columns):

        self.validate_name(schema_name)
        self.validate_name(table_name)

        columns_sql = ", ".join(
            [f"{col['name']} {col['type']}" for col in columns]
        )

        sql = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
            {columns_sql}
        );
        """

        self.run(sql)
    


    








