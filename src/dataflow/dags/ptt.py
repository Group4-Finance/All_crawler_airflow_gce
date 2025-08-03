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
    ptt,
)

import requests
from bs4 import BeautifulSoup

def get_latest_index(board):
        url = f"https://www.ptt.cc/bbs/{board}/index.html"
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'zh-TW,zh;q=0.9',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive'
        }
        cookies = {'over18': '1'}

        res = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        a = soup.find_all("a", {"class": "btn wide"})

        if len(a) > 1:
            href = a[1]["href"]
        elif len(a) == 1:
            href = a[0]["href"]
        else:
            raise ValueError("❌ 無法取得分頁連結")

        split_href = href.split("/")
        if not split_href or "index" not in split_href[-1]:
            raise ValueError("❌ 無法解析 index")

        latest_index = split_href[-1].replace("index", "").replace(".html", "")
        return int(latest_index) + 1

board = "stock"
end_index = get_latest_index(board)
start_index = 954

# 定義 DAG，並用 with 語法將任務放入 DAG 環境中
with airflow.DAG(
    # DAG 的唯一名稱，用來識別 DAG
    dag_id="ptt",
    # 套用預設參數設定
    default_args=DEFAULT_ARGS,
    # 不自動排程，只能手動或外部觸發
    # schedule_interval="0 9-14 * * 1-5",
    schedule_interval= None,
    concurrency=1,
    # 限制同時執行的最大 DAG 實例數
    max_active_runs=MAX_ACTIVE_RUNS,
    # 禁止補跑過去未執行的排程
    catchup=False,
) as dag:
    tasks = []
    while start_index < end_index:
         task = ptt(start_index)
         start_index = start_index + 1
         tasks.append(task)
    # 建立並註冊 DockerOperator 任務到 DAG
    