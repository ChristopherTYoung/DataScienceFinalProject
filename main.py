from utils import get_necessary_col_names_from_csv
from cleaning import clean_nulls_care, remove_incomplete
from mtgsdk import Card
from merge import add_card_data
import matplotlib.pyplot as plt
import pandas as pd
import requests
import csv
import gzip
import os

# Install requirements
# pip install -r requirements.txt

draft_data_file_name = "draft.csv"
draft_data_file_path = f"./{draft_data_file_name}"
card_data_file_name = "card_data.csv"
card_data_file_path = f"./{card_data_file_name}"

mtg_set = "FDN"
mtg_set_for_card_data = mtg_set.lower()

draft_url = f"https://17lands-public.s3.amazonaws.com/analysis_data/draft_data/draft_data_public.{mtg_set}.PremierDraft.csv.gz"
card_data_url = f"https://api.scryfall.com/cards/search?q=set:{mtg_set_for_card_data}"

if not os.path.exists(draft_data_file_path):
    response = requests.get(draft_url)
    print("Fetching data")
    with open(f"draft_data_public.{mtg_set}.PremierDraft.csv.gz", mode="wb") as file:
        file.write(response.content)

    with gzip.open(f"draft_data_public.{mtg_set}.PremierDraft.csv.gz", "rb") as f:
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

df = pd.concat(chunks, ignore_index=True)



card_data = pd.read_csv("card_data.csv")
df = clean_nulls_care(df, columns_to_use)
df = remove_incomplete(df)
df = add_card_data(df, card_data)
df = df.drop_duplicates(["draft_id", "pack_number", "pick_number"])

print(df.head())




# add color and rarity

card_column_names = [col for col in df.columns if col.startswith("pack_card_")]

pack_number = 0
early_pick_number = 0
wheeled_pick_number = 8
player_index = "player_inx"
pick_suffix = (
    f"_{pack_number}_{early_pick_number}",
    f"_{pack_number}_{wheeled_pick_number}",
)

df_early_pick_number = df[
    (df["pick_number"] == early_pick_number) & (df["pack_number"] == pack_number)
].copy()
df_wheeled_pick_number = df[
    (df["pick_number"] == wheeled_pick_number) & (df["pack_number"] == pack_number)
].copy()

df_early_pick_number[player_index] = df_early_pick_number.groupby("draft_id").cumcount()
df_wheeled_pick_number[player_index] = df_wheeled_pick_number.groupby(
    "draft_id"
).cumcount()

df_of_early_and_wheeled_picks = df_early_pick_number.merge(
    df_wheeled_pick_number, on=["draft_id", player_index], suffixes=pick_suffix
)

percent_wheeled = {}

for card in card_column_names:
    card_col_early = card + pick_suffix[0]
    card_col_wheeled = card + pick_suffix[1]

    relevant_rows_for_cards = df_of_early_and_wheeled_picks[
        df_of_early_and_wheeled_picks[card_col_early] >= 1
    ]

    wheeled_count = (relevant_rows_for_cards[card_col_wheeled] >= 1).sum()

    if len(relevant_rows_for_cards) > 0:
        percent = (wheeled_count / len(relevant_rows_for_cards)) * 100
    else:
        percent = 0
    percent_wheeled[card] = percent

plt.figure(figsize=(10, 6))
plt.bar(percent_wheeled.keys(), percent_wheeled.values(), color="skyblue")
plt.xlabel("Card")
plt.ylabel("Percent Wheeled (%)")
plt.title("Percent Wheeled by Card")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
