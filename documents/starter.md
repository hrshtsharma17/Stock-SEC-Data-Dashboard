# Starter

This pipeline serves multiple purposes: it not only facilitates dashboard creation but also offers exposure to a variety of tools, skill development opportunities, and the potential to assist others. This versatile tool can be applied to diverse data sources, including interactions on social networks, financial trading data, common crawl data, and more.

## How the Pipeline Works

This project is centered around a single Directed Acyclic Graph (DAG) responsible for extracting SEC EDGAR data using the [SEC EDGAR API](https://www.sec.gov/edgar/sec-api-documentation).

The pipeline is configured to extract data from the past 24 hours and store it in a CSV file with fields such as CIK and ticker name. 

**NOTE:** SEC data is not updated as frequently. However, the 24 hour cycle has been mentioned as a general rerun period so feel free to play around with this.

Subsequently, this CSV is directly loaded into an AWS S3 bucket (cloud storage) and then copied to AWS Redshift (cloud data warehouse) for further analysis.

The entire process is orchestrated using Apache Airflow within a Docker container, eliminating the need for manual Airflow setup.

In addition to the components managed by Airflow, two other elements are part of this project:

* **Data Transformation:** We utilize dbt to connect to our data warehouse and perform data transformations. While our primary purpose is to gain familiarity with dbt and build our skills, it also plays a crucial role in data preparation.

* **Visualization:** The final step involves connecting a Business Intelligence (BI) tool to our data warehouse and creating visualizations. Google Data Studio is recommended, but you are free to choose an alternative tool that suits your preferences.

Proceed to the next step to embark on this exciting journey.

---

[Next Step](aws-setup.md)

or

[Back to README](../README.md)