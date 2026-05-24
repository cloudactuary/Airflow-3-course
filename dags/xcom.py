from airflow.sdk import dag, task, Context

@dag
def dag_xcom():

    @task
    def t1() -> int:
    # def t1(context: Context):
        x = 42
        return x # - the same as  `context['ti'].xcom_push(key = "my_key", value = x)`


    @task
    def t2(val: int):
    # def t2(context: Context):
        # val = context['ti'].xcom_pull(task_id = 't1', key = "my_key")

        print(val)


    val = t1()
    t2(val)
    # t1() >> t2()

dag_xcom()
