from utils import get_necessary_col_names_from_csv
import matplotlib.pyplot as plt
import pandas as pd
import requests
import gzip
import os

# --- Fetch and Load Data ---
file_name = "draft.csv"
file_path = f"./{file_name}"
mtg_set = "FDN"
url = f"https://17lands-public.s3.amazonaws.com/analysis_data/draft_data/draft_data_public.{mtg_set}.PremierDraft.csv.gz"

if not os.path.exists(file_path):
    response = requests.get(url)
    print("Fetching data")
    with open(f"draft_data_public.{mtg_set}.PremierDraft.csv.gz", mode="wb") as file:
        file.write(response.content)

    with gzip.open(f"draft_data_public.{mtg_set}.PremierDraft.csv.gz", "rb") as f:
        file_content = f.read()
        with open("draft.csv", "wb") as f_out:
            f_out.write(file_content)
else:
    print("draft.csv already exists")

chunk_size = 10000
total_chunks = 100
total_number_of_rows = chunk_size * total_chunks
number_of_rows_processed = 0

chunks = []
columns_to_use = get_necessary_col_names_from_csv(file_name)

for chunk in pd.read_csv(
    file_name,
    usecols=columns_to_use,
    chunksize=chunk_size,
):
    number_of_rows_processed += chunk_size
    print(
        f"processed (another) {number_of_rows_processed} rows out of {total_number_of_rows}"
    )
    filtered_chunk = chunk[~chunk["pick_number"].isin([6, 7])]
    chunks.append(filtered_chunk)
    if number_of_rows_processed >= total_number_of_rows:
        break

df = pd.concat(chunks, ignore_index=True)

# --- Analysis Setup ---
card_column_names = [col for col in df.columns if col.startswith("pack_card_")]
player_index = "player_inx"
early_wheel_pairs = [(0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13)]
pack_numbers = [0, 1, 2]

# --- Matrix Plot Setup ---
fig, axes = plt.subplots(nrows=3, ncols=6, figsize=(24, 12), sharey=True)
fig.suptitle("Percent Wheeled by Card (Matrix View)", fontsize=18)

# --- Matrix Loop ---
for row_idx, pack_number in enumerate(pack_numbers):
    for col_idx, (early_pick_number, wheeled_pick_number) in enumerate(
        early_wheel_pairs
    ):
        pick_suffix = (
            f"_{pack_number}_{early_pick_number}",
            f"_{pack_number}_{wheeled_pick_number}",
        )

        df_early_pick_number = df[
            (df["pick_number"] == early_pick_number)
            & (df["pack_number"] == pack_number)
        ].copy()
        df_wheeled_pick_number = df[
            (df["pick_number"] == wheeled_pick_number)
            & (df["pack_number"] == pack_number)
        ].copy()

        df_early_pick_number[player_index] = df_early_pick_number.groupby(
            "draft_id"
        ).cumcount()
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
            total = len(relevant_rows_for_cards)
            percent = (wheeled_count / total) * 100 if total > 0 else 0
            percent_wheeled[card] = percent

        # --- Plotting ---
        ax = axes[row_idx][col_idx]
        ax.bar(percent_wheeled.keys(), percent_wheeled.values(), color="skyblue")
        ax.set_title(
            f"Pack {pack_number} | Picks {early_pick_number}/{wheeled_pick_number}",
            fontsize=10,
        )
        ax.tick_params(axis="x", rotation=90)
        if col_idx == 0:
            ax.set_ylabel("Percent Wheeled (%)")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
