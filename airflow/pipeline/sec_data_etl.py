import sys
import datetime
import pandas as pd
import requests

"""
Part of Airflow DAG. 
Script will connect to SEC API and extract the latest information of companies filings for the latest quarter.
"""

HEADER = {'User-Agent': "youremail@address.com"}
META_DATA_FIELDS = ['tickers', 'category', 'sicDescription', 'entityType', 'exchanges',
       'filingCount', 'cik', 'name', 'stateOfIncorporation', 'sic',
       'latestRevenueFilingDate', 'latestRevenueQ10Value',
       'latestAssestsFilingDate', 'latestAssestsQ10Value', 'created_utc']


def get_company_tickers():
    company_tickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=HEADER
    )

    if company_tickers.status_code==200:
        company_tickers = company_tickers.json()
    else:
        company_tickers = {}

    return company_tickers

def get_sec_companies():
    """Getting the list of companies from SEC API"""
    company_tickers = get_company_tickers()
    company_data = pd.DataFrame(company_tickers).T
    company_data["cik_str"] = company_data.cik_str.astype(str).str.zfill(10)

    return company_data

def get_company_filing_meta(cik):
    company_filing_meta = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=HEADER
    )

    if company_filing_meta.status_code==200:
        company_filing_meta = company_filing_meta.json()
    else:
        company_filing_meta = {}

    return company_filing_meta

def company_metadata(cik):
    """Getting the company metadata information from SEC API and extracting target keys info"""
    target_keys = set(["cik",
    "entityType",
    'sic',
    'sicDescription',
    'name',
    'tickers',
    'exchanges',
    'category',
    'stateOfIncorporation',
    'filingCount'])

    raw_meta_data = get_company_filing_meta(cik)

    metadata = {}
    for key in target_keys:
        if key in raw_meta_data:
            metadata[key] = raw_meta_data[key]
        else:
            metadata[key] = None
    
    if raw_meta_data['filings'].get('files'):
        metadata['filingCount'] = int(raw_meta_data['filings']['files'][-1]['filingCount'])
    else:
        metadata['filingCount'] = 0
    
    metadata['tickers'] = metadata['tickers'][-1] #TODO: Workround for array error in redshift. Find a fix
    metadata['exchanges'] = metadata['exchanges'][-1] #TODO: Workround for array error in redshift. Find a fix
    metadata['cik'] = int(metadata['cik'])
    if not metadata['sic']:
        metadata['sic'] = -1

    return metadata

def get_company_facts(cik):
    company_facts = requests.get(
    f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
    headers=HEADER
    )

    if company_facts.status_code==200:
        company_facts = company_facts.json()
    else:
        company_facts = {}

    return company_facts

def get_company_concept(cik):
    company_concept = requests.get(
    (
    f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'
     f'/us-gaap/Assets.json'
    ),
    headers=HEADER
    )

    if company_concept.status_code==200:
        company_concept = company_concept.json()
    else:
        company_concept = {}

    return company_concept

def get_company_assets(cik):
    """Extracting Assets information per latest filing"""
    company_concept_dict = get_company_concept(cik)
    latest_unit_doc = company_concept_dict.get('units', {"USD":[{"filed":None, "val":-1}]})
    if latest_unit_doc.get('USD'):
        latest_unit_doc = latest_unit_doc['USD'][-1]
    elif latest_unit_doc.get('EUR'):
        latest_unit_doc = latest_unit_doc['EUR'][-1]
        latest_unit_doc["val"] *= 1.08 #TODO: Add dynamic currency exchange check

    filing_date = latest_unit_doc["filed"]
    assets_val = int(latest_unit_doc["val"])

    return {"latestAssestsFilingDate": filing_date, 
            "latestAssestsQ10Value": assets_val}

def get_company_revenue(cik):
    """Extracting Revenue information per latest filing"""
    company_facts_dict = get_company_facts(cik)

    try:
        latest_unit_doc = company_facts_dict['facts']['us-gaap'].get('Revenues', {"units":{"USD":[{"filed":None, "val":-1}]}})['units']['USD'][-1]
    except KeyError:
        latest_unit_doc = {"filed":None, "val":-1}

    filing_date = latest_unit_doc["filed"]
    revenue_val = latest_unit_doc["val"]

    return {"latestRevenueFilingDate": filing_date, 
            "latestRevenueQ10Value": revenue_val}

def load_to_csv(file_name, df):
    """Save extracted data to CSV file in /tmp folder"""
    df.to_csv(f"/tmp/{file_name}.csv", index=False)

def main():
    """Extract SEC data and load to CSV"""
    try:
        output_name = sys.argv[1]
    except IndexError as e:
        print(f"Command line argument not passed. Error {e}")
        sys.exit(1)
    
    all_companies = get_sec_companies()[:4]
    all_companies_df = pd.DataFrame(columns=META_DATA_FIELDS)
    for _, company_row in all_companies.iterrows():
        cik = company_row["cik_str"]
        data = company_metadata(cik)
        revenue_data = get_company_revenue(cik)
        assets_data = get_company_assets(cik)

        for key in revenue_data: data[key] = revenue_data[key]
        for key in assets_data: data[key] = assets_data[key]

        data["created_utc"] = datetime.datetime.now()
        all_companies_df = all_companies_df.append(data, ignore_index=True)

    load_to_csv(output_name, all_companies_df)

if __name__ == "__main__":
    main()