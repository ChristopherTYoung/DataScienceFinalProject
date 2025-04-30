from cleaning import clean_nulls_care, remove_incomplete
from file_reading import read_draft_data, get_necessary_col_names_from_csv
from constants import draft_data_file_name
from merge import add_card_data
from models import ata_vs_mana_cost
from compact import compact
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
card_data = pd.read_csv(card_data_file_name)
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
# df = add_card_data(draft_df, card_data)

print(draft_df.head())
# ata_vs_mana_cost(card_data)

# card_column_names = [col for col in draft_df.columns if col.startswith("pack_card_")]
