from typing import List
import pandas as pd


# add columns color, rarity, mana cost, etc.
def add_card_data(df: pd.DataFrame, card_data: pd.DataFrame, columns_to_add: List[str]) -> pd.DataFrame:
    if 'name' not in df.columns:
        raise KeyError("The 'name' column is missing in the first DataFrame.")
    if 'name' not in card_data.columns:
        raise KeyError("The 'name' column is missing in the second DataFrame.")
    if 'name' not in columns_to_add:
        columns_to_add += ['name']
    combined_df = df.merge(card_data[columns_to_add], 
                            on='name', 
                            how='left')
    return combined_df
