
from urllib import response
import requests
from datetime import datetime, timedelta
from parse_entsoe_xml import parse_entsoe_xml

# Sett inn din egen API-nøkkel (Security Token fra ENTSO-E)
API_TOKEN = "ab23f244-da60-4bff-8a00-062135e2a42b"

# URL til ENTSO-E API
url = "https://web-api.tp.entsoe.eu/api"



def fetch_activated_balancing_energy(controlArea_Domain, periodStart, periodEnd, api_token):
    url = "https://web-api.tp.entsoe.eu/api"
    params = {
        "securityToken": api_token,
        "documentType": "A83",         # Aggregated Activated Balancing Energy
        "businessType": "A98",         # mFRR
        "controlArea_Domain": controlArea_Domain,
        "periodStart": periodStart,
        "periodEnd": periodEnd
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print("Data hentet fra API:")
        for post in data[:5]:  # viser bare de 5 første
            print(f"ID: {post['id']} - Title: {post['title']}")
    else:
        print(f"Feil: {response.status_code}")


# Eksempel på bruk for balansemarkedet (Activated Balancing Energy 17.1.E)
API_TOKEN = "ab23f244-da60-4bff-8a00-062135e2a42b"
periodStart = "201501010000"
periodEnd = "201501052300"



# Hent data måned for måned fra 2015 til 2025 for NO1
import pandas as pd
from dateutil.relativedelta import relativedelta

API_TOKEN = "ab23f244-da60-4bff-8a00-062135e2a42b"
controlArea_Domain_NO1 = "10YNO-1--------2"
controlArea_Domain_NO2 = "10YNO-2--------T"
controlArea_Domain_NO3 = "10YNO-3--------J"
controlArea_Domain_NO4 = "10YNO-4--------9"
controlArea_Domain_NO5 = "10Y1001A1001A48H"
start_year = 2015
end_year = 2025

dfs = []
current = pd.Timestamp(f"{start_year}-01-01 00:00")
end = pd.Timestamp(f"{end_year}-01-01 00:00")
while current < end:
    periodStart = current.strftime("%Y%m%d%H%M")
    next_month = current + relativedelta(months=1)
    periodEnd = (next_month - pd.Timedelta(hours=1)).strftime("%Y%m%d%H%M")
    df = fetch_activated_balancing_energy(controlArea_Domain_NO5, periodStart, periodEnd, API_TOKEN)
    if df is not None and not df.empty:
        dfs.append(df)
    current = next_month

if dfs:
    df_all = pd.concat(dfs, ignore_index=True)
    print(df_all.head())
    df_all.to_csv("parsed_balancing_energy_NO5.csv", index=False)
    print("Lagret til parsed_balancing_energy_NO5.csv")
else:
    print("Ingen data hentet for perioden.")
    print("Lagret til parsed_entsoe.csv")
