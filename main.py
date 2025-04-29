from utils import get_necessary_col_names_from_csv
from cleaning import clean_nulls_care, remove_incomplete
from merge import add_card_data
import matplotlib.pyplot as plt
import pandas as pd
import requests
import csv
import gzip
import os

from constants import (
    draft_data_file_name,
    draft_data_file_path,
    card_data_file_name,
    card_data_file_path,
    draft_url,
    card_data_url,
    draft_zip_file_name,
)

# Install requirements
# pip install -r requirements.txt

if not os.path.exists(draft_data_file_path):
    response = requests.get(draft_url)
    print("Fetching data")
    with open(draft_zip_file_name, mode="wb") as file:
        file.write(response.content)

    with gzip.open(draft_zip_file_name, "rb") as f:
        file_content = f.read()
        with open(draft_data_file_name, "wb") as f_out:
            f_out.write(file_content)
else:
    print("draft.csv already exists")

if not os.path.exists(card_data_file_path):
    print("Fetching card data...")
    fields = ["name", "mana_cost", "colors", "color_identity", "rarity"]

    with open(card_data_file_name, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        # Fetching all the pages of card data
        # The Scryfall API returns paginated results, so we need to loop through the pages
        next_url = card_data_url
        while next_url:
            response = requests.get(next_url)
            data = response.json()
            cards = data["data"]

            for card in cards:
                writer.writerow({field: card.get(field, "") for field in fields})

            next_url = data.get("next_page") if data.get("has_more") else None
else:
    print(f"{card_data_file_path} already exists")

chunk_size = 10000
total_chunks = 100
total_number_of_rows = chunk_size * total_chunks
number_of_rows_processed = 0

chunks = []
columns_to_use = get_necessary_col_names_from_csv(draft_data_file_name)

for chunk in pd.read_csv(
    draft_data_file_name, usecols=columns_to_use, chunksize=chunk_size
):
    number_of_rows_processed += chunk_size
    print(
        f"processed (another) {number_of_rows_processed} rows out of {total_number_of_rows}"
    )
    filtered_chunk = chunk[(chunk["pick_number"] != 6) & (chunk["pick_number"] != 7)]
    chunks.append(filtered_chunk)
    if number_of_rows_processed >= total_number_of_rows:
        break

dirty_draft_df = pd.concat(chunks, ignore_index=True)
card_data = pd.read_csv("card_data.csv")

draft_no_nulls_df = clean_nulls_care(dirty_draft_df, columns_to_use)
draft_duplicates_df = remove_incomplete(draft_no_nulls_df)
draft_df = draft_duplicates_df.drop_duplicates(
    ["draft_id", "pack_number", "pick_number"]
)
df = add_card_data(draft_df, card_data)

print(df.head())

# card_column_names = [col for col in draft_df.columns if col.startswith("pack_card_")]
