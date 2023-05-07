from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime

"""
DAG to execute pipeline for extracting SEC data, loading into AWS S3, 
and copying to AWS Redshift
"""

# Output name of extracted file. This be passed to each
# DAG task so they know which file to process
output_name = datetime.now().strftime("%Y%m%d")

# Run our DAG daily and ensure DAG run success, 
# Note: The SEC data is not high frequency and changes per quarter
#       Hence, the daily run is just for checking the workings of DAGs as they should.
#TODO: After testing change run frequency to longer period gap.


# once Airflow is started, as it will try to "catch up"
schedule_interval = "@daily"
start_date = days_ago(1)

default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}

with DAG(
    dag_id="sec_data_pipeline",
    description="SEC Company Data ELT",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
    tags=["SecETL"],
) as dag:

    extract_sec_data = BashOperator(
        task_id="extract_sec_data",
        bash_command=f"python /opt/airflow/pipeline/sec_data_etl.py {output_name}",
        dag=dag,
    )
    extract_sec_data.doc_md = "Extract relevant SEC data and store as CSV"

    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command=f"python /opt/airflow/pipeline/upload_data_s3.py {output_name}",
        dag=dag,
    )
    upload_to_s3.doc_md = "Upload SEC CSV data to S3 bucket"

    copy_to_redshift = BashOperator(
        task_id="copy_to_redshift",
        bash_command=f"python /opt/airflow/pipeline/S3_to_redshift.py {output_name}",
        dag=dag,
    )
    copy_to_redshift.doc_md = "Copy S3 CSV file to Redshift table"

extract_sec_data >> upload_to_s3 >> copy_to_redshift