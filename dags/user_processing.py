from airflow.sdk import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


@dag
def user_processing():
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

user_processing()
