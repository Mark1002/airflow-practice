"""Dataprep dags."""
from datetime import timedelta
from airflow.utils import timezone
from airflow import DAG

args = {
    'owner': 'cloudmile',
    'start_date': timezone.utcnow() - timedelta(hours=3),
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

with DAG(dag_id='dataprep_dag', default_args=args) as dag:
    pass
