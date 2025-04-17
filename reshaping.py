import pandas as pd
import matplotlib.pyplot as plt
from constants import columns_to_use

pack_number_we_want = 0

data_csv_title = "draft.csv"

chunk_size = 10000
total_chunks = 100

chunks = []

for chunk in pd.read_csv(
    data_csv_title,
    usecols=columns_to_use,
    chunksize=chunk_size,
):
    print(len(chunks))
    filtered_chunk = chunk[chunk["pick_number"] != 7]
    chunks.append(filtered_chunk)

df = pd.concat(chunks, ignore_index=True)

# We don't care about the following
# expansion
# event_typ
# draft_time
# event_match_wins
# event_match_losses
# pick_maindeck_rate
# pick_sideboard_in_rate

# Maybe we care about
# draft_id str
# rank categorical
# pack number int starting at 0
# pick categorical (card name)

# And then there is pack_card_(CARDNAME) - in quotes if it has a comma in the name

# user_n_games_bucket means that users have so many games played
# Helpful article: https://joelnitta.com/posts/2023-12-31_17lands-intro/

# 14 picks per pack

card_columns = [col for col in df.columns if col.startswith("pack_card_")]

df_pick0 = df[(df["pick_number"] == 0) & (df["pack_number"] == 0)].copy()
df_pick8 = df[(df["pick_number"] == 8) & (df["pack_number"] == 0)].copy()

df_pick0["player_idx"] = df_pick0.groupby("draft_id").cumcount()
df_pick8["player_idx"] = df_pick8.groupby("draft_id").cumcount()

# Suffixes make it so we can see the difference pick 0 and pick 8.
# Clean idea - if the card was in pick 8 but not pick 0, it is bad
merged = df_pick0.merge(df_pick8, on=["draft_id", "player_idx"], suffixes=("_0", "_8"))

percent_wheeled = {}

for card in card_columns:
    card_col_0 = card + "_0"
    card_col_8 = card + "_8"

    relevant_rows_for_cards = merged[merged[card_col_0] >= 1]

    # Is there ever a two?
    wheeled_count = (relevant_rows_for_cards[card_col_8] >= 1).sum()

    # Calculate percentage over all drafts
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
