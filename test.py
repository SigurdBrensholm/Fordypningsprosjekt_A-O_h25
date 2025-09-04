# API - TOKEN generert til Sigurd: ab23f244-da60-4bff-8a00-062135e2a42b
import pandas as pd
import requests

API_KEY = "ab23f244-da60-4bff-8a00-062135e2a42b"
BASE_URL = "https://web-api.tp.entsoe.eu/api"

# Kun NO2
zone = "NO2"
domain = "10YNO-2--------T"

doc = "A82"           # Aggregated Activated Balancing Energy
business_type = "A96" # FCR
# Test med én måned for å unngå for stor respons
start = "202109200000"
end   = "202109202300"  # Slutt 31. januar 2015

url = (
    f"{BASE_URL}"
    f"?documentType={doc}"
    f"&businessType={business_type}"
    f"&controlArea_Domain={domain}"
    f"&periodStart={start}"
    f"&periodEnd={end}"
    f"&securityToken={API_KEY}"
    f"&psrType={"A04"}"
)

print(f"Henter {doc} for {zone} fra {start} til {end} ...")
r = requests.get(url, timeout=120)  # økt timeout for stor respons

if r.status_code == 200 and r.content:
    try:
        df = pd.read_xml(r.content)
        df["zone"] = zone
        df["dataset"] = doc
        print(f"Data hentet: {len(df)} rader")
        df.to_csv("FCR_Offers_NO2_2015_2025.csv", index=False)
        print("Lagret til FCR_Offers_NO2_2015_2025.csv")
    except Exception as e:
        print(f"Kunne ikke parse XML: {e}")
else:
    print(f"Feil: status {r.status_code}, {r.text[:200]}")
