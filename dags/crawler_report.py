"""Crawler report dags."""
import pendulum

from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator

local_tz = pendulum.timezone('Asia/Taipei')

args = {
    'owner': 'bignet',
    'start_date': datetime(2020, 2, 5, tzinfo=local_tz)
}

with DAG(
    dag_id='crawler_report', default_args=args, schedule_interval='@daily'
) as dag:
    set_up_bigscrapy_project_task = SSHOperator(
        ssh_conn_id='ssh_big_airflow',
        task_id='set_up_bigscrapy_project',
        command="""
        docker run -d --name bigscrapy_projects_airflow \
        bigregistry.buygta.today/bigscrapy_projects
        """
    )

    tear_down_bigscrapy_project_task = SSHOperator(
        ssh_conn_id='ssh_big_airflow',
        task_id='tear_down_bigscrapy_project',
        command="""
        docker rm -f bigscrapy_projects_airflow
        """
    )

    set_up_bigscrapy_project_task >> tear_down_bigscrapy_project_task
