# AWS

We will utilize Amazon Web Services (AWS) to store our sec data in the cloud. Specifically, we will use two AWS services:

* [Simple Storage Service (S3)](https://aws.amazon.com/s3/): This is an object storage service. When we extract data from sec, we'll store it in a CSV format and push it to an S3 Bucket as an object. Think of a Bucket as a folder and an object as a file. This allows us to securely store all our raw data in the cloud.

* [Redshift](https://aws.amazon.com/redshift/): This is a Data Warehousing service that utilizes Massively Parallel Processing (MPP) technology. Redshift can execute operations on large datasets at high speeds. It's built on PostgreSQL, which means we can use SQL to perform operations.

While we could use a local database like PostgreSQL for our project, working with cloud tools like AWS services is considered good practice.

To begin using AWS, follow these steps:

## Setup

1. **Create an AWS Account:** Start by setting up a personal [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Follow the instructions provided in this [guide](https://aws.amazon.com/getting-started/guides/setup-environment/module-one/) to set up your account with the free tier.

2. **Secure Your Account:** Ensure the security of your AWS account by following these [steps](https://aws.amazon.com/getting-started/guides/setup-environment/module-two/). This includes setting up Multi-Factor Authentication (MFA) for the root user. The root user has access to all AWS resources, so it's crucial to secure it. Additionally, consider setting up an Identity and Access Management (IAM) user with specific permissions. In production environments, it's best practice to limit the use of the root account.

3. **Setup AWS CLI:** Configure the AWS Command Line Interface (CLI) by following this [guide](https://aws.amazon.com/getting-started/guides/setup-environment/module-three/). This CLI setup allows you to interact with AWS services from the command line. By the end of this setup, you should have a `.aws` folder in your home directory containing a `credentials` file that looks like this:

    ```config
    [default]
    aws_access_key_id = XXXX
    aws_secret_access_key = XXXX
    ```

    This configuration enables your scripts to interact with AWS without requiring you to include access keys directly in your scripts.

---

[Previous Step](starter.md) | [Next Step](infra-setup.md)

or

[Back to README](../README.md)