"""Example DAG demonstrating the usage of the extraction via Inlets and Outlets."""

import pendulum
import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.lineage.entities import Table, File

def create_table(cluster, database, name):
    return Table(
        database=database,
        cluster=cluster,
        name=name,
    )

t1 = create_table("c1", "d1", "t1")
t2 = create_table("c1", "d1", "t2")
t3 = create_table("c1", "d1", "t3")
t4 = create_table("c1", "d1", "t4")
f1 = File(url = "http://randomfile")

with DAG(
    dag_id='example_operator',
    schedule_interval='0 0 * * *',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    dagrun_timeout=datetime.timedelta(minutes=60),
    params={"example_key": "example_value"},
) as dag:
    task1 = BashOperator(
        task_id='task_1_with_inlet_outlet',
        bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        inlets=[t1, t2],
        outlets=[t3],
    )

    task2 = BashOperator(
        task_id='task_2_with_inlet_outlet',
        bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        inlets=[t3, f1],
        outlets=[t4],
    )

    task1 >> task2
    
if __name__ == "__main__":
    dag.cli()
