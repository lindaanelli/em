from pymongo import MongoClient
import pandas as pd

conn = MongoClient("localhost", 27017)
print("Connected successfully!")

scopus_csv = pd.read_csv("scopus.csv")
scopus_csv.rename(columns={'Art. No.': 'Art No'}, inplace=True)
data = scopus_csv.to_dict(orient="index")

for i in range(len(data)):
    data[str(i)] = data.pop(i)


scopus = conn.scopus
collection = scopus["Simonini"]
collection.insert_one(data)
