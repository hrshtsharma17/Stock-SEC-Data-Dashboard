# Data Visualisation 

We now want to visualise our data. It's up to you how to do this. 

Below I've provided some basic instructions on connecting Redshift to [PowerBI](https://powerbi.microsoft.com/en-gb/) and [Google Data Studio](https://datastudio.google.com).

Feel free to use the default table in Redshift (i.e. sec_table) or the newly transformed one we created with dbt (i.e. sec_transformed).

> Google Data Studio is the better option for a personal project, as reports created here can freely and easily be shared.

## Google Data Studio

1. Navigate [here](https://datastudio.google.com) and follow the setup instructions. 
1. Click `Create` on the top right, then `Report`
1. Under `Connect to data` search for `Amazon Redshift`
1. Enter the relevant details and click `Authenticate`
1. Select your table

You can now feel free to create some visualisations. Some tutorial/guides [here](https://support.google.com/datastudio/answer/6283323?hl=en). Here's an example of mine:

You can then publicly share your report by navigating to Share > Manage access.

## PowerBI

For PowerBI, you'll need to use Windows OS and install PowerBI Desktop. If you're on Mac or Linux, you can consider a virtualisation software like [virtualbox](https://www.virtualbox.org) to use Windows.

To connect Redshift to PowerBI:
 
1. Create an account with PowerBI. If you don't have a work or school email address, consider setting up an account with a [temporary email address](https://tempmail.net), as it won't accept Gmail and other services used for personal accounts. 
1. Open PowerBI and click `Get Data`.
1. Search for `Redshift` in the search box and click `Connect`.
1. Enter your Redshift server/host name, and the name of the database (e.g. dev) and click `OK`.
1. Enter the username (e.g. awsuser) and password for the database, and then select the relevant table you'd like to load in. 

You can now feel free to create some visualisations. Some tutorials/guides [here](https://docs.microsoft.com/en-us/learn/powerplatform/power-bi).

---

[Previous Step](dbt.md)

or

[Back to README](../README.md)