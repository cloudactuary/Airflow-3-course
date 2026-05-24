from airflow.sdk import dag, task, task_group


@dag
def groups():

    @task
    def a():
        return 42

    @task_group(
        default_args = {
            "retries": 2
        }
    )
    def b_c_group(val: int):
        @task
        def b(my_val: int):
            print(my_val + 42)

        @task
        def c():
            print("c")

        b(val) >> c()

    b_c_group(a())


groups()
