from airflow.sdk import dag, task
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag
def dag_user_processing():

    # Execution task
    create_table = SQLExecuteQueryOperator(
        task_id = "create_table",
        conn_id = "pg_conn",
        sql = """
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
        """
    )

    # Sensor Task
    @task.sensor(poke_interval = 30, timeout = 600)
    def is_api_available() -> PokeReturnValue:
        import requests
        resp = requests.get("https://randomuser.me/api")
        if resp.status_code == 200:
            return PokeReturnValue(is_done = True, xcom_value = resp.json())
        else:
            return PokeReturnValue(is_done = False, xcom_value = None)

    is_api_available()
    
dag_user_processing()

