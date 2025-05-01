from cleaning import clean_nulls_care, remove_incomplete
from compact import compact
from file_reading import read_draft_data, get_necessary_col_names_from_csv
from constants import draft_data_file_name
from merge import add_card_data
from models import ata_vs_mana_cost, win_rate_vs_ata, gns_vs_ata, logistic_regression_model
from compile import compile_all_drafts
import pandas as pd
from file_creation import (
    create_draft_data_if_not_exists,
    create_card_data_if_not_exists,
)
from constants import card_data_file_name

# Install requirements
# pip install -r requirements.txt

create_draft_data_if_not_exists()
create_card_data_if_not_exists()

draft_data_columns_to_use = get_necessary_col_names_from_csv(draft_data_file_name)

dirty_draft_df = read_draft_data(draft_data_columns_to_use)
card_data_df = pd.read_csv(card_data_file_name)
print("read card data")

draft_no_nulls_df = clean_nulls_care(dirty_draft_df, draft_data_columns_to_use)
print("cleaned nulls")
draft_duplicates_df = remove_incomplete(draft_no_nulls_df)
print("removed incomplete drafts")
complex_draft_df = draft_duplicates_df.drop_duplicates(
    ["draft_id", "pack_number", "pick_number"]
)
print("removed duplicates")
draft_df = compact(complex_draft_df)
print("compacted draft data")

stats_df = compile_all_drafts(draft_df, card_data_df)
stats_df["rarity_numeric"] = stats_df["rarity"].map({"common": 1, "uncommon": 2, "rare": 3, "mythic": 4})
print(stats_df.columns)

model = logistic_regression_model(stats_df, ["ATA", "shared_colors_count", "rarity_numeric", "ATA_avg", "pick_number"])
# , "GP WR_avg", "shared_color_identity_count"
print(model.summary())
# ata_vs_mana_cost(card_data)
# gns_vs_ata(card_data)

# card_column_names = [col for col in draft_df.columns if col.startswith("pack_card_")]
