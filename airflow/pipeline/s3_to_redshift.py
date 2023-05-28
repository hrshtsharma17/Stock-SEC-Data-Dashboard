import configparser
import pathlib
import psycopg2
import sys
from psycopg2 import sql

"""
Part of DAG. Upload S3 CSV data to Redshift. Script will load data into temporary table in Redshift, delete 
records with the same post ID from main table, then insert these from temp table (along with new data) 
to main table. This means that if we somehow pick up duplicate records in a new DAG run,
the record in Redshift will be updated to reflect any changes in that record, if any (e.g. higher score or more comments).
"""

# Parse our configuration file
script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/configuration.conf")

# Store our configuration variables
USERNAME = parser.get("aws_config", "redshift_username")
PASSWORD = parser.get("aws_config", "redshift_password")
HOST = parser.get("aws_config", "redshift_hostname")
PORT = parser.get("aws_config", "redshift_port")
REDSHIFT_ROLE = parser.get("aws_config", "redshift_role")
DATABASE = parser.get("aws_config", "redshift_database")
BUCKET_NAME = parser.get("aws_config", "bucket_name")
ACCOUNT_ID = parser.get("aws_config", "account_id")
TABLE_NAME = "sec_table"

# Check command line argument passed
try:
    output_name = sys.argv[1]
except Exception as e:
    print(f"Command line argument not passed. Error {e}")
    output_name = "20230904"
    #sys.exit(1)

# Our S3 file access path
file_path = f"s3://{BUCKET_NAME}/{output_name}.csv"
role_string = f"arn:aws:iam::{ACCOUNT_ID}:role/{REDSHIFT_ROLE}"

# Create Redshift table if it doesn't exist
sql_create_table = sql.SQL(
    """CREATE TABLE IF NOT EXISTS {table} (
                            tickers varchar(max),
                            category varchar(max),
                            sicDescription varchar(max),      
                            entityType varchar(max),
                            exchanges varchar(max), 
                            filingCount int,
                            cik varchar PRIMARY KEY,                                                                                                                                  
                            name varchar(max),
                            stateOfIncorporation varchar(20),                              
                            sic int,
                            latestRevenueFilingDate date,
                            latestRevenueQ10Value bigint,
                            latestAssestsFilingDate date,
                            latestAssestsQ10Value bigint,
                            created_utc timestamp
                        );"""                  
).format(table=sql.Identifier(TABLE_NAME))

# If ID already exists in table, we remove it and add new ID record during load.
create_temp_table = sql.SQL(
    "CREATE TEMP TABLE staging_table (LIKE {table});"
).format(table=sql.Identifier(TABLE_NAME))
sql_copy_to_temp = f"COPY staging_table FROM '{file_path}' iam_role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV;"
delete_from_table = sql.SQL(
    "DELETE FROM {table} USING staging_table WHERE {table}.cik = staging_table.cik;"
).format(table=sql.Identifier(TABLE_NAME))
insert_into_table = sql.SQL(
    "INSERT INTO {table} SELECT * FROM staging_table;"
).format(table=sql.Identifier(TABLE_NAME))
drop_temp_table = "DROP TABLE staging_table;"


def main():
    """Upload file form S3 to Redshift Table"""
    rs_conn = connect_to_redshift()
    load_data_into_redshift(rs_conn)


def connect_to_redshift():
    """Connect to Redshift instance"""
    try:
        rs_conn = psycopg2.connect(
            dbname=DATABASE, user=USERNAME, password=PASSWORD, host=HOST, port=PORT
        )
        return rs_conn
    except Exception as e:
        print(f"Unable to connect to Redshift. Error {e}")
        sys.exit(1)

def load_data_into_redshift(rs_conn):
    """Load data from S3 into Redshift"""
    with rs_conn:

        cur = rs_conn.cursor()
        cur.execute(sql_create_table)
        cur.execute(create_temp_table)
        cur.execute(sql_copy_to_temp)
        cur.execute(delete_from_table)
        cur.execute(insert_into_table)
        cur.execute(drop_temp_table)

        rs_conn.commit()

if __name__ == "__main__":
    main()