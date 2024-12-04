from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
# Define a function to modify the CSV
def modify_csv_column_name(**kwargs):
    # File path (replace with your actual file path)
    input_file_path = 'file:///mounts/shared-volume/shared/spark/file1.csv'
    # Read the CSV file
    df = pd.read_csv(input_file_path)
    # Rename a column (example: renaming 'old_column' to 'new_column')
    df.rename(columns={‘degree’:’new_degree'}, inplace=True)
    # Save the modified CSV
    df.show()
    print(f"File modified")
# Define the DAG
with DAG(
    'modify_csv_column_name_dag',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
    },
    description='A DAG to modify a column name in a CSV file',
    schedule_interval=None,  # Set to None for manual execution
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    # Define the PythonOperator
    modify_csv_task = PythonOperator(
        task_id='modify_csv_task',
        python_callable=modify_csv_column_name,
    )
    modify_csv_task
