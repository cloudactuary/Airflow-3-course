from airflow.sdk import dag, task
from airflow.sdk.bases.sensor import PokeReturnValue
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

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
        resp = requests.get("https://raw.githubusercontent.com/marclamberti/datasets/refs/heads/main/fakeuser.json")
        if resp.status_code == 200:
            return PokeReturnValue(is_done = True, xcom_value = resp.json())
        else:
            return PokeReturnValue(is_done = False, xcom_value = None)

    # this example how to use python code w/o PythonOperator
    @task
    def extract_user(fake_user):
        return {
            "id": fake_user["id"],
            "firstname": fake_user["personalInfo"]["firstName"],
            "lastname": fake_user["personalInfo"]["lastName"],
            "email": fake_user["personalInfo"]["email"]
        }
    
    COLUMNS_USER = ["id", "firstname", "lastname", "email"]


    @task
    def proceess_user(user_info_dict):
        with open("/tmp/users.csv", "w") as f:
            f.write(','.join(user_info_dict.keys()) + "\n")
            f.write(','.join(map(str, [user_info_dict[k] for k in COLUMNS_USER])) + "\n")
        
        with open("/tmp/users.csv", "r") as f:
            print("file itself")
            print(f.read())

    @task
    def store_user():
        hook = PostgresHook(postgres_conn_id = "pg_conn")
        hook.copy_expert(
            sql = f"COPY users ({','.join(COLUMNS_USER)}) FROM stdin WITH DELIMITER ',' CSV HEADER;",
            filename = "/tmp/users.csv"
        )

    # fake_user = is_api_available()
    # user_info = extract_user(fake_user)
    # proceess_user(user_info)
    # store_user()

    proceess_user(extract_user(create_table >> is_api_available())) >> store_user()
    
dag_user_processing()

