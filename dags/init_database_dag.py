# import sys 
# from pathlib import Path
# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.python import PythonOperator


# AIRFLOW_HOME = Path ("/opt/airflow")

# if str(AIRFLOW_HOME) not in sys.path:
#     sys.path.append(str(AIRFLOW_HOME))

# from plugins.operators.create_schema_operator import CreateSchemaOperator
# from plugins.operators.create_database_operator import CreateDatabaseOperator
# from plugins.operators.create_table_operator import CreateTableOperator

# default_args = {
#     "owner": "airflow",
#     "retries": 1,
#     "retry_delay": timedelta(minutes=1),
# }


# with DAG(
#     dag_id="init_database",
#     default_args=default_args,
#     start_date=datetime(2026, 5, 17),
#     # manual trigger only
#     schedule=None,
#     catchup=False,
#     tags=["init", "database"]
# ) as dag:
   
#     # create_bronze = CreateSchemaOperator(
#     #     task_id="create_bronze_schema",
#     #     postgres_conn_id="postgres_conn_id",
#     #     database_name="cdc_db",
#     #     schema_name="bronze",
#     #     table_name="orders_cdc_log",
#     #     columns=[
#     #         {"name": "order_id", "type": "INT"},
#     #         {"name": "changed_at", "type": "TIMESTAMP"},
#     #         {"name": "operation", "type": "VARCHAR(10)"}
#     #     ]
       
#     # )
#     create_database = CreateDatabaseOperator(
#         task_id="create_database",
#         postgres_conn_id="postgres_conn_id",
#         database_name="test"
#     )

#     create_schema  = CreateSchemaOperator(
#         task_id="create_schema",
#         postgres_conn_id="postgres_conn_id",
#         schema_name="test_schema"
#     )

#     create_table = CreateTableOperator(
#         task_id="create_table",
#         postgres_conn_id="postgres_conn_id",
#         schema_name="test_schema",
#         table_name="test_table",
#         columns=[
#             {"name": "order_id", "type": "INT"},
#             {"name": "changed_at", "type": "TIMESTAMP"},
#             {"name": "operation", "type": "VARCHAR(10)"}
#         ]
#     )


#     create_database >> create_schema >> create_table




