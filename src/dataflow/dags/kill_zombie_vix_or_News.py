from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pendulum import timezone 
from dataflow.etl.kill_zom import (
    # 建立並回傳一個 DockerOperator 任務
    clear_stuck_dag_runs_NEWS,
)

local_tz = timezone("Asia/Taipei")
# today = datetime.now().strftime('%Y%m%d')

with DAG(
    dag_id="maintenance_clear_stuck_runs_NEWS",
    start_date=datetime(2022, 1, 1, tzinfo=local_tz),
    schedule_interval="50 23 * * *",  # 每 20 分鐘掃一次
    catchup=False,
    max_active_runs=1,
) as dag:   
    clear_stuck = PythonOperator(
    task_id="clear_stuck_dag_runs_NEWS",
    python_callable=clear_stuck_dag_runs_NEWS,
    queue = "All_crawler",
)