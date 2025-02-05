from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.github_pr_utils import insert_data_to_database, get_latest_review_timestamp
from dags.send_email import send_email


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    default_args=default_args,
    dag_id="send_emails_v01",
    description="send top 5 open pr to my personal email", 
    start_date=datetime(2025, 1, 20),
    schedule_interval="@daily"
) as dag:
    task1 = PythonOperator(
        task_id="insert_data_to_database",
        python_callable=insert_data_to_database()
    )

    task2 = PythonOperator(
        task_id="get_latest_review_timestamp",
        python_callable=get_latest_review_timestamp()
    )

    task3 = PythonOperator(
        task_id="send_email",
        python_callable=send_email()
    )

    task1 >> task2 >> task3