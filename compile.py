from typing import List, Optional
import pandas as pd 
from merge import add_card_data
import numpy as np
def compile_cards(df: pd.DataFrame, card_data: pd.DataFrame, columns_to_add: List[str], row: int, *, columns_for_average: Optional[List[str]] = None) -> pd.DataFrame:
    newdf = pd.DataFrame({"name": df["cards_in_pack"][row]})
    newdf = add_card_data(newdf, card_data, columns_to_add)
    newdf["draft_id"], newdf["pack_number"], newdf["pick_number"] = df["draft_id"].iloc[row], df["pack_number"].iloc[row], df["pick_number"].iloc[row]
    if(columns_for_average != None):
            for row in newdf:
                packs_without = df["cards_in_pack"][row].copy().remove(newdf[row])
                print(packs_without) 
                packs_without = pd.DataFrame({"name": packs_without
                                              })
                packs_without = add_card_data(packs_without, card_data, columns_for_average)
                for col in columns_for_average:
                    if(not newdf.columns.__contains__(col+'_avg')):
                        newdf[col+'_avg']=0
                    newdf[col+'_avg'][row]=np.mean(packs_without[col])
    return newdf