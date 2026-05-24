from airflow.sdk import dag, task, Context
from typing import Dict, Any

@dag
def dag_xcom():

    @task
    def t1() -> Dict[str, Any]:
        return {
            "val1": 42,
            "val2": "hello"
        }


    @task
    def t2(val: Dict[str, Any]):

        print(val["val1"])
        print(val["val2"])


    val = t1()
    t2(val)
    # t1() >> t2()

dag_xcom()
