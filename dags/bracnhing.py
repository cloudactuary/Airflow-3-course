from airflow.sdk import dag, task


@dag
def branching_dag():

    @task
    def a():
        return 1

    @task.branch
    def b(val: int):
        return ['eq_1'] if val == 1 else ['neq_1']

    @task
    def eq_1(val: int):
        print(f"equal 1: {val}")
    
    @task
    def neq_1(val: int):
        print(f"not equal 1: {val}")


    val = a()
    b(val) >> [eq_1(val), neq_1(val)]


branching_dag()
