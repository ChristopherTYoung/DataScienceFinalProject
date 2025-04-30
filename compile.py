from typing import List, Optional
import pandas as pd 
from merge import add_card_data
import numpy as np
def compile_cards(df: pd.DataFrame, card_data: pd.DataFrame, columns_to_add: List[str], row: int, *, columns_for_average: Optional[List[str]] = None) -> pd.DataFrame:
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