import boto3
import pandas as pd
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from spotify_etl import extract_raw_playlist_data#, transform_raw_data

s3_client = boto3.client('s3')
target_bucket_name = 'spotify-airflow-bucket'

def extract_data():
    df = extract_raw_playlist_data()
    now = datetime.now()
    date_now_string = now.strftime('%Y-%m-%d')
    file_str = f"spotify_playlist_raw_data_{date_now_string}"
    df.to_csv(f"{file_str}.csv", index=False)
    output_file_path = f"/home/ubuntu/{file_str}.csv"
    return [output_file_path, file_str]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 24),
    'email': ['steven.lennartsson@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

# with DAG('spotify_etl_dag',
#          default_args=default_args,
#          # schedule_interval = @weekly,
#          catchup=False) as dag:
    
#         extract_spotify_data = PythonOperator(
#             task_id= 'tsk_extract_spotify_data',
#             # python_callable=extract_data
#         )

df = extract_raw_playlist_data()
print(df)