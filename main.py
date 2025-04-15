import requests
import zipfile
import gzip
import pandas as pd

url = "https://17lands-public.s3.amazonaws.com/analysis_data/draft_data/draft_data_public.FDN.PremierDraft.csv.gz"

response = requests.get(url)

with open("draft_data_public.FDN.PremierDraft.csv.gz", mode="wb") as file:
    file.write(response.content)

with gzip.open('draft_data_public.FDN.PremierDraft.csv.gz', 'rb') as f:
    file_content = f.read()
    with open('draft.csv', 'wb') as f_out:
        f_out.write(file_content)

df = pd.read_csv('draft.csv', nrows=100000)

print(df.head())
print(df.describe())