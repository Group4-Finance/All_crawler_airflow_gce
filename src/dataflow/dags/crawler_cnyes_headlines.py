# 匯入 Airflow 核心模組
import airflow


# 匯入自定義的常數設定，用於統一管理 DAG 參數與執行限制
from dataflow.constant import (
    # 預設參數，例如 owner、start_date、retries 等
    DEFAULT_ARGS,
    # 限制同一時間同一 DAG 最多允許幾個執行實例
    MAX_ACTIVE_RUNS,
)

# 匯入自定義的 DockerOperator 任務建立函式
from dataflow.etl.docker_operator import (
    # 建立並回傳一個 DockerOperator 任務
    crawler_cnyes_headlines,
)


month_list = [
    '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
 '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12',
 '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12',
 '2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', '2023-12',
 '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
 '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07'
]


# 定義 DAG，並用 with 語法將任務放入 DAG 環境中
with airflow.DAG(
    # DAG 的唯一名稱，用來識別 DAG
    dag_id="crawler_cnyes_headlines",
    # 套用預設參數設定
    default_args=DEFAULT_ARGS,
    # schedule_interval="0 9-14 * * 1-5",
    schedule_interval= None,
    concurrency=1,
    # 限制同時執行的最大 DAG 實例數
    max_active_runs=MAX_ACTIVE_RUNS,
    # 禁止補跑過去未執行的排程
    catchup=False,

) as dag:
    tasks = []
    for month in month_list:
        task = crawler_cnyes_headlines(month)
        print(f"crawler_cnyes_headlines({month}) 完成 ")
        tasks.append(task)
    # 建立並註冊 DockerOperator 任務到 DAG
        