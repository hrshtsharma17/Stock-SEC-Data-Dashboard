import sys
import boto3
import botocore.exceptions
import configparser
import pathlib

"""
Part of Airflow DAG. 
Upload the csv data generated using EDGAR API to S3.
"""

def read_config(config_path):
    parser = configparser.ConfigParser()
    parser.read(config_path)
    return parser

def get_config_value(config, section, key):
    return config.get(section, key)

def validate_input(output_name):
    if not output_name:
        print("Command line argument not passed.")
        sys.exit(1)

def connect_to_s3():
    try:
        conn = boto3.resource("s3")
        return conn
    except Exception as e:
        print(f"Can't connect to S3. Error: {e}")
        sys.exit(1)

def create_bucket_if_not_exists(conn, bucket_name, aws_region):
    try:
        conn.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            conn.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": aws_region},
            )

def upload_file_to_s3(conn, bucket_name, key, filename):
    conn.meta.client.upload_file(
        Filename=filename, Bucket=bucket_name, Key=key
    )

def main():
    config_path = pathlib.Path(__file__).parent.resolve() / "configuration.conf"
    config = read_config(config_path)
    BUCKET_NAME = get_config_value(config, "aws_config", "bucket_name")
    AWS_REGION = get_config_value(config, "aws_config", "aws_region")

    try:
        output_name = sys.argv[1]
    except IndexError as e:
        print(f"Command line argument not passed. Error {e}")
        sys.exit(1)

    FILENAME = f"/tmp/{output_name}.csv"
    KEY = FILENAME

    validate_input(output_name)

    conn = connect_to_s3()
    create_bucket_if_not_exists(conn, BUCKET_NAME, AWS_REGION)
    upload_file_to_s3(conn, BUCKET_NAME, KEY, FILENAME)

if __name__ == "__main__":
    main()