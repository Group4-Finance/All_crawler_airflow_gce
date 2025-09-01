from airflow import DAG
from airflow.operators.python import PythonOperator
from pendulum import timezone 
from datetime import datetime
from dataflow.etl.kill_zom import (
    # 建立並回傳一個 DockerOperator 任務
    clear_stuck_dag_runs_ETF,
)

local_tz = timezone("Asia/Taipei")
# today = datetime.now().strftime('%Y%m%d')

with DAG(
    dag_id="maintenance_clear_stuck_runs_ETF",
    start_date=datetime(2022, 1, 1, tzinfo=local_tz),
    schedule_interval="*/30 8-10 * * 1-5",  # 每 20 分鐘掃一次
    catchup=False,
    max_active_runs=1,
) as dag:   
    clear_stuck = PythonOperator(
    task_id="clear_stuck_dag_runs_ETF",
    python_callable=clear_stuck_dag_runs_ETF,
    queue = "All_crawler",
)