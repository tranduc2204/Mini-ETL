import sys 
from pathlib import Path
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


AIRFLOW_HOME = Path ("/opt/airflow")

if str(AIRFLOW_HOME) not in sys.path:
    sys.path.append(str(AIRFLOW_HOME))

from plugins.operators.postgres_operator import CreateSchemaOperator
from scripts.bronze.bronze_extract import bronze_extract


default_args = {
    "owner": "airflow",
    "retries": 0,
    "retry_delay" : timedelta(minutes=5),
}


with DAG(
    dag_id="cdc_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 5, 17),
    schedule_interval="*/5 * * * *",
    catchup=False,
) as dag:
    
    bronze = PythonOperator(
        task_id="bronze_ingest",
        python_callable=bronze_extract,
    )

    create_schema = CreateSchemaOperator(
        task_id = "create_schema",
        postgres_conn_id = "postgres_conn_id",
        layer_name = "bronze"
    )

    create_schema >> bronze

    #  create_bronze = CreateSchemaOperator(
    #     task_id="create_bronze_schema",
    #     postgres_conn_id="postgres_default",
    #     layer_name="bronze"
    # )

    # create_silver = CreateSchemaOperator(
    #     task_id="create_silver_schema",
    #     postgres_conn_id="postgres_default",
    #     layer_name="silver"
    # )

    # create_gold = CreateSchemaOperator(
    #     task_id="create_gold_schema",
    #     postgres_conn_id="postgres_default",
    #     layer_name="gold"
    # )

    # (
    #     create_bronze
    #     >> create_silver
    #     >> create_gold
    # )














