import datetime
from airflow import models
from airflow.operators import bash_operator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from google.cloud import bigquery, storage
import google.auth
import os

ENV = os.environ.get('ENV')  # test or prod
PROJECT_ID = 'project-{env}'.format(env=ENV)
BUCKET_NAME = 'bucket_name_{env}'.format(env=ENV)
BUCKET = 'gs://{bucket_name}'.format(bucket_name=BUCKET_NAME)
DATASET_BQ = 'dataset_name'
DATASET_ID = "{project_id}.{dataset}".format(project_id=PROJECT_ID, dataset=DATASET_BQ)


default_dag_args = {
    'start_date': datetime.datetime(2021, 4, 14),
    'provide_context': True
}

dag = models.DAG(
    'dag_name',
    schedule_interval="00 12 * * *",
    default_args=default_dag_args
)

credentials, project = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery", ]
)

# Construct a BigQuery client object.
client = bigquery.Client(credentials=credentials, project=project)
dataset = client.get_dataset(DATASET_ID)

