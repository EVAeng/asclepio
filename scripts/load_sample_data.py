import numpy as np
import pandas as pd

from pymongo import MongoClient


# Extra cleaning
data = pd.read_csv("dentists.csv")
data.drop('Unnamed: 0', axis=1, inplace=True)
data["specialties"] = data["specialization"].apply(lambda x: [x])
data.drop('specialization', axis=1, inplace=True)
data["middle_name"].fillna("", inplace=True)
data["address_2nd_line"].fillna("", inplace=True)

# Add coluumns with random values:
np.random.seed(42)
data['price'] = np.random.randint(9, 106, data.shape[0])
data['rate'] = np.random.uniform(1, 5, data.shape[0])
data['reviews'] = [[]] * data.shape[0]

# Load to Mongo

records = data.to_dict("records")

client = MongoClient()
asclepio_db = client["asclepio"]
doctors_collection = asclepio_db["doctors"]

doctors_collection.insert_many(records)
