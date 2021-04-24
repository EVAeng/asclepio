import pandas as pd

from pymongo import MongoClient


# Extra cleaning
data = pd.read_csv("dentists.csv")
data.drop('Unnamed: 0', axis=1, inplace=True)
data["specialization"] = data["specialization"].apply(lambda x: [x])
data["middle_name"].fillna("", inplace=True)
data["address_2nd_line"].fillna("", inplace=True)

records = data.to_dict("records")

client = MongoClient()
asclepio_db = client["asclepio"]
doctors_collection = asclepio_db["doctors"]

doctors_collection.insert_many(records)
