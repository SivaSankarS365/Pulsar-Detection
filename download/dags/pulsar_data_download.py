import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
import zipfile

# Define some variables
DATA_URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00372/HTRU2.zip'
DATA_DIR = os.path.expanduser('~/Desktop/CS5830/')
ZIP_PATH = os.path.join(DATA_DIR, 'HTRU2.zip')
CSV_PATH = os.path.join(DATA_DIR, 'HTRU_2.csv')

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 18),
    'retries': 1,
    'retry_delay': timedelta(days=1),
}

# Define the DAG
dag = DAG(
    'pulsar_data_download',
    default_args=default_args,
    description='A simple DAG to download and extract pulsar data',
    schedule_interval=timedelta(days=1),
)

def download_data():
    """Download the dataset from the given URL."""
    os.makedirs(DATA_DIR, exist_ok=True)
    response = requests.get(DATA_URL)
    with open(ZIP_PATH, 'wb') as f:
        f.write(response.content)

def extract_data():
    """Extract the dataset to the specified directory."""
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)
    os.rename(os.path.join(DATA_DIR, 'HTRU_2.csv'), CSV_PATH)

# Define the tasks
download_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    dag=dag,
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

# Set the task dependencies
download_task >> extract_task