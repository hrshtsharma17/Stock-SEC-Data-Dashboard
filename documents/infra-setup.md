# AWS Infrastructure Setup

We will use an infrastructure-as-code tool called `Terraform` to quickly set up (and tear down) our AWS resources using code. Please note that Terraform is not limited to AWS; it works with multiple cloud providers.

If you are new to Terraform, you can find a quick introduction in [this tutorial](https://learn.hashicorp.com/terraform?utm_source=terraform_io).

Using Terraform, we will create the following AWS resources:

* **Redshift Cluster**: 
  - Redshift is a columnar data warehousing solution offered by AWS. It will serve as the end destination for our data.

* **IAM Role for Redshift**:
  - This role will be assigned to Redshift, granting it permission to read data from S3.

* **S3 Bucket**:
  - This object storage will store our extracted sec data.

* **Security Group**:
  - This security group will be applied to Redshift, allowing all incoming traffic so our dashboard can connect to it. Note that in a real production environment, it's not recommended to allow all traffic into your resource.

## Setup

1. **Install Terraform**:

    You can find installation instructions for your OS [here](https://learn.hashicorp.com/tutorials/terraform/install-cli).

2. **Change into the Terraform Directory**:

    Navigate to the Terraform directory:

    ```bash
    cd ~/stock-sec-data-dashboard/terraform
    ```

3. **Open the `variables.tf` File**:

4. **Fill in Default Parameters**:

    - Specify a master DB user password for Redshift. Ensure it meets password complexity requirements as it may show up in logs and the Terraform state file.

    - Specify a unique bucket name that adheres to S3 bucket naming constraints (e.g., `<yourfullname>_sec_bucket`).

    - Specify a region (e.g., `eu-west-2`). You can find a list of regions [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html). Ideally, choose a region close to your location.

5. **Update `.gitignore`** (Optional):

    To prevent accidentally committing sensitive details, you may want to modify your `.gitignore` file. Remove the `!*.tf` line if necessary.

6. **Initialize Terraform**:

    While in the Terraform directory, download the AWS Terraform plugin:

    ```bash
    terraform init
    ```

7. **Create AWS Resources**:

    Create a plan based on `main.tf` and execute the planned changes to create resources in AWS:

    ```bash
    terraform apply
    ```

8. **Destroy Resources** (Optional):

    If needed, you can terminate the resources:

    ```bash
    terraform destroy
    ```

In the [AWS Console](https://aws.amazon.com/console/), you can now view your Redshift cluster, IAM Role, and S3 Bucket. You can also manually delete or customize them here and query any Redshift databases using the query editor. Ensure you specify the correct region in the top right-hand side of the AWS console when looking for your Redshift cluster.

---

[Previous Step](aws-setup.md) | [Next Step](config.md)

or

[Back to README](../README.md)