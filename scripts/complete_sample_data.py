import concurrent.futures

import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict


def get_country_from_address(add):
    add1, city, state, add2 = add
    url = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"

    headers = CaseInsensitiveDict()
    headers["User-Agent"] = "Mozilla/5.0"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = f"companyName=&address1={add1}&address2={add2}&city={city}O&state={state}&urbanCode=&zip="

    resp = requests.post(url, headers=headers, data=data)
    addr = ""

    if resp.status_code == 200:
        address_list = resp.json().get("addressList")

        if address_list:
            addr = address_list[0].get("zip5")

    return addr


# Read
target_columns = """Classification\nName Prefix\nCredential\nLast Name\nFirst Name\nMiddle Name\nGender\nBusiness Address 1st Line\nBusiness Address 2nd Line\nBusiness Address City\nBusiness Address State\nBusiness Address Zip Code\nBusiness Address Phone\nLicense Number\nNPI""".split(
    "\n")
data = pd.read_csv(
    "/Users/reysantos7/Downloads/Dental_Providers_CA_122300000X.csv", usecols=target_columns)
# Rename in place
data.rename(columns={'Classification': 'Specialization',
                     'Business Address 1st Line': 'Address 1st Line',
                     'Business Address 2nd Line': 'Address 2nd Line',
                     'Business Address City': 'Address City',
                     'Business Address State': 'Address State',
                     'Business Address Zip Code': 'Address Zip Code',
                     'Business Address Phone': 'Address Phone'}, inplace=True)

data.columns = [val.lower().replace(' ', "_") for val in data.columns.values]

with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    print("getting zipcodes")
    get_country_from_address
    zipcodes = [(add1, city, state, add2) for add1, add2, city, state in zip(data['address_1st_line'], data['address_2nd_line'],
                                                                             data['address_city'], data['address_state'])]
    f = executor.map(get_country_from_address, zipcodes)
    res = []
    for z in f:
        res.append(z)
    data["address_zip_code"] = pd.Series(res)  # 3 elements

data.to_csv("dentists.csv")
print(data.head(10))
# 'https://tools.usps.com/tools/app/ziplookup/zipByAddress' --data 'companyName=&address1=131 W GRAND AVE&address2=SUITE B&city=EL SEGUNDO&state=CA&urbanCode=&zip=' -H "User-Agent: Mozilla/5.0"
