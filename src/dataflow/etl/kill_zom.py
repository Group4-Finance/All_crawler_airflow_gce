from airflow.models import DagRun
from airflow.utils.state import State
from datetime import  timedelta
from airflow.utils.session import provide_session
from airflow.utils.timezone import utcnow
etf_dag_id = ["ETF_signal", "ETF_PremiumDiscount", "ETF_historyprice", "vix"]

@provide_session
def clear_stuck_dag_runs_ETF(session=None, **kwargs):
    for dag_id in etf_dag_id:
        stuck_runs = (
            session.query(DagRun)
            .filter(DagRun.dag_id == dag_id)
            .filter(DagRun.state == State.RUNNING)
            .filter(DagRun.execution_date < utcnow() - timedelta(minutes=20))
            .all()
        )
        for run in stuck_runs:
            print(f"清除卡住的dag: {run.dag_id}, run: {run.execution_date}")
            run.set_state(State.FAILED)
            session.merge(run)
    session.commit()


news_dag_id = ["MagaBank_NEWS_daily", "ptt_daily", "crawler_cnyes_headlines_daily"]

@provide_session
def clear_stuck_dag_runs_NEWS(session=None, **kwargs):
    for dag_id in news_dag_id:
        stuck_runs = (
            session.query(DagRun)
            .filter(DagRun.dag_id == dag_id)
            .filter(DagRun.state == State.RUNNING)
            .filter(DagRun.execution_date < utcnow() - timedelta(minutes=10))
            .all()
        )
        for run in stuck_runs:
            print(f"清除卡住的dag: {run.dag_id}, run: {run.execution_date}")
            run.set_state(State.FAILED)
            session.merge(run)
    session.commit()
    