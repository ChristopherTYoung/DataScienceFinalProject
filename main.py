import requests
import gzip
import pandas as pd
import os

# change path 
file_path = "./draft.csv"
url = "https://17lands-public.s3.amazonaws.com/analysis_data/draft_data/draft_data_public.FDN.PremierDraft.csv.gz"

response = requests.get(url)

if not os.path.exists(file_path):
    print("Fetching data")
    with open("draft_data_public.FDN.PremierDraft.csv.gz", mode="wb") as file:
        file.write(response.content)

    with gzip.open('draft_data_public.FDN.PremierDraft.csv.gz', 'rb') as f:
        file_content = f.read()
        with open('draft.csv', 'wb') as f_out:
            f_out.write(file_content)
else:
    print("draft.csv already exists")

df = pd.read_csv('draft.csv', nrows=100000)

print(df.head())
print(df.describe())