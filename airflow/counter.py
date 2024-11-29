from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago

with DAG(
    'counter',
    start_date=days_ago(1),
    schedule='*/1 * * * *',
    catchup=False,
    is_paused_upon_creation=False,
    max_active_runs=1,
    description='DAG that generates a new count value equal to 1.'
):

    query1 = PostgresOperator(
        task_id='if_not_exists',
        postgres_conn_id='example_db',
        sql='''
        CREATE TABLE IF NOT EXISTS counts (
            value INTEGER
        );'''
    )

    query2 = PostgresOperator(
        task_id='inc',
        postgres_conn_id='example_db',
        sql='''
        INSERT INTO counts (value)
            VALUES (1) 
        '''
    )

query1 >> query2
