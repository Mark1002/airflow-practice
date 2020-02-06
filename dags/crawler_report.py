"""Crawler report dags."""
import pendulum
import logging
from datetime import datetime
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import PythonOperator

local_tz = pendulum.timezone('Asia/Taipei')

args = {
    'owner': 'bignet',
    'start_date': datetime(2020, 2, 4, tzinfo=local_tz)
}

dag = DAG(
    dag_id='crawler_report',
    default_args=args,
    schedule_interval='@daily'
)


def show_message(**kwargs):
    """Show message."""
    logging.debug('hello world!')


# start_message_task = PythonOperator(
#     task_id='start_message',
#     python_callable=show_message,
#     provide_context=True,
#     dag=dag,
#     op_kwargs={'message': 'start crawler report'}
# )

crawler_test_task = DockerOperator(
    task_id='crawler_test',
    image='centos:latest',
    api_version='auto',
    auto_remove=True,
    command="/bin/sleep 30",
    docker_url="unix:///var/run/docker.sock",
    network_mode="bridge",
    dag=dag
)
