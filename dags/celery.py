from time import sleep
from airflow.sdk import dag, task

@dag
def dag_celery():

    @task
    def a():
        sleep(2)
        
    @task
    def b():
        sleep(2)

    @task
    def c():
        sleep(2)

    @task
    def d():
        sleep(2)


    a() >> [b(), c()] >> d()

dag_celery()
