from typing import List
import pandas as pd


# add columns color, rarity, mana cost, etc.
def add_card_data(df: pd.DataFrame, card_data: pd.DataFrame, columns_to_add: List[str]) -> pd.DataFrame:
    combined_df = df.merge(card_data[columns_to_add], 
                            on='name', 
                            how='left')
    return combined_df
