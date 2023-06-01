# Config Setup

In the next step, you'll need to create a configuration file with your specific details. The extract and load scripts in our pipeline will utilize the information provided in this configuration file. A configuration template has already been provided in the airflow folder, similar to the one mentioned below.

## Setup

1. **Create Configuration File**:

    Create a configuration file named `configuration.conf` under `~/stock-sec-data-dashboard/airflow/pipeline`:

    ```bash
    touch ~/stock-sec-data-dashboard/airflow/pipeline/configuration.conf
    ```

2. **Edit Configuration**:

    Copy and paste the following content into your `configuration.conf` file:

    ```conf
    [aws_config]
    bucket_name = XXXXX
    redshift_username = awsuser
    redshift_password = XXXXX
    redshift_hostname = XXXXX
    redshift_role = RedShiftLoadRole
    redshift_port = 5439
    redshift_database = dev
    account_id = XXXXX
    aws_region = XXXXX
    ```

3. **Replace `XXXXX` Values**:

    Replace the `XXXXX` values in the `aws_config` section with your specific configuration details.

    - If you need a reminder of your `aws_config` details, navigate back to the terraform folder and run the following command. It will output the values you need to store under `aws_config`. Make sure to remove any `"` characters from the strings.

        ```bash
        terraform output
        ```

---

[Previous Step](infra-setup.md) | [Next Step](docker-airflow.md)

or

[Back to README](../README.md)
