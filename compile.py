from typing import List, Optional
import pandas as pd 
from merge import add_card_data
import numpy as np
# Only do the first 5
def compile_cards(df: pd.DataFrame, card_data: pd.DataFrame, columns_to_add: List[str], row: int, *, columns_for_average: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Takes in the compact dataframe, a row index, and a list of values to use for averaging.
    Returns a new DataFrame where each row corresponds to an individual card in the pack 
    along with its associated data.

    Args:
        df (pd.DataFrame): The compact input DataFrame containing draft data.
        card_data (pd.DataFrame): the card data used
        row (int): The index of the row to extract pack data from.
        columns_to_add (List[str]): columns to add from the card_data
        *optional
        columns_for_average: List of column names to average over. 

    Returns:
        pd.DataFrame: Expanded DataFrame with individual card rows and calculated averages.
    """
    newdf = pd.DataFrame({"name": df["cards_in_pack"][row]})
    newdf = add_card_data(newdf, card_data, columns_to_add)
    newdf["draft_id"], newdf["pack_number"], newdf["pick_number"] = df["draft_id"].iloc[row], df["pack_number"].iloc[row], df["pick_number"].iloc[row]
    newdf = newdf.set_index('name')
    if(columns_for_average != None):
        for newrow in newdf.index:
            packs_without = df["cards_in_pack"][row].copy()
            packs_without.remove(newrow)
            packs_without = pd.DataFrame({'name': packs_without})
            packs_without = add_card_data(packs_without, card_data, ['name'] + columns_for_average)
            
            for col in columns_for_average:
                avg_col_name = col + '_avg'
                if avg_col_name not in newdf.columns:
                    newdf[avg_col_name] = None
                
                newdf.at[newrow, avg_col_name] = packs_without[col].mean()
    return newdf