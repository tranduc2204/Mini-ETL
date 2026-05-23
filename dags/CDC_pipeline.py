import sys 
from pathlib import Path
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


AIRFLOW_HOME = Path ("/opt/airflow")

if str(AIRFLOW_HOME) not in sys.path:
    sys.path.append(str(AIRFLOW_HOME))

from plugins.operators.create_schema_operator import CreateSchemaOperator
from scripts.bronze.bronze_extract import bronze_extract
from scripts.silver.silver_cdc_history import process_bronze_to_silver
from    scripts.silver.silver_orders import silver_orders   


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

    silver = PythonOperator(
        task_id="silver_process",
        python_callable=process_bronze_to_silver,
    )
    silver_end = PythonOperator(
        task_id="silver_end",
        python_callable=silver_orders,
    )       

    bronze >> silver >> silver_end
   








