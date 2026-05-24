
from airflow.sdk import dag, task

@dag
def sql_dag():
    @task.sql(
        conn_id = "conn_airflow"
    )
    def get_n_xcoms():
        return "SELECT count(*) FROM xcom"
    
    get_n_xcoms()

sql_dag()
