"""Crawler report dags."""
import pendulum
import logging
from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.python_operator import PythonOperator

local_tz = pendulum.timezone('Asia/Taipei')

args = {
    'owner': 'bignet',
    'start_date': datetime(2020, 2, 4, tzinfo=local_tz)
}


def show_message(**kwargs):
    """Show message."""
    logging.debug('hello world!')


with DAG(
    dag_id='crawler_report', default_args=args, schedule_interval='@daily'
) as dag:
    start_message_task = PythonOperator(
        task_id='start_message',
        python_callable=show_message,
        provide_context=True,
        op_kwargs={'message': 'start crawler report'}
    )

    set_up_bigscrapy_project_task = SSHOperator(
        ssh_conn_id='ssh_big_ariflow',
        task_id='set_up_bigscrapy_project',
        command='echo "hello world" > summary.txt'
    )
