"""Crawler report dags."""
import requests

from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.ssh_hook import SSHHook


args = {
    'owner': 'bignet',
    'start_date': datetime.now() - timedelta(hours=1),
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}


def get_crawler_report() -> str:
    """Get crawler report."""
    ssh = SSHHook(ssh_conn_id='ssh_big_airflow')
    client = ssh.get_conn()
    stdin, stdout, stderr = client.exec_command("""
    docker exec `docker ps  --filter name=bigscrapy_projects_airflow -q` \
    sh -c 'cat /bigcrawler-scrapy/summary.txt'
    """)
    message = "".join([line for line in stdout.readlines()])
    print(f'crawler_report: {message}')
    return message


def send_mattermost():
    """Send report message to mattermost."""
    message = get_crawler_report()
    webhook_url = 'https://chat.buygta.today/hooks/zbr8kctkytnebk76pcrshyysba'
    requests.post(webhook_url, json={'text': message})


with DAG(
    dag_id='crawler_report', default_args=args,
    schedule_interval='0 * * * *', max_active_runs=1,
    concurrency=1
) as dag:
    set_up_bigscrapy_project_task = SSHOperator(
        ssh_conn_id='ssh_big_airflow',
        task_id='set_up_bigscrapy_project',
        command="""
        [ "$(docker ps --filter name=bigscrapy_projects_airflow -q)" ] && \
        docker rm -f bigscrapy_projects_airflow
        docker run -d --name bigscrapy_projects_airflow \
        bigregistry.buygta.today/bigscrapy_projects
        """
    )

    run_pytest_task = SSHOperator(
        ssh_conn_id='ssh_big_airflow',
        task_id='run_pytest',
        command="""
        docker exec `docker ps  --filter name=bigscrapy_projects_airflow -q` \
        sh -c 'cd /bigcrawler-scrapy && pipenv install --dev && \
        pipenv run pytest -rf --tb=no | tee summary.txt && \
        rm -rf tests/cassettes'
        """
    )

    send_report_task = PythonOperator(
        task_id='send_report',
        python_callable=send_mattermost
    )

    tear_down_bigscrapy_project_task = SSHOperator(
        ssh_conn_id='ssh_big_airflow',
        task_id='tear_down_bigscrapy_project',
        command="""
        docker rm -f bigscrapy_projects_airflow
        """
    )

    set_up_bigscrapy_project_task >> run_pytest_task
    run_pytest_task >> send_report_task
    send_report_task >> tear_down_bigscrapy_project_task
