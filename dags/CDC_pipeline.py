import sys 
from pathlib import Path
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


AIRFLOW_HOME = Path ("/opt/airflow")

if str(AIRFLOW_HOME) not in sys.path:
    sys.path.append(str(AIRFLOW_HOME))

from scripts.bronze_extract import bronze_extract


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

















