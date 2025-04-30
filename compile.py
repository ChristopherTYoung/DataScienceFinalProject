from typing import List, Optional
import pandas as pd
from has_wheeled import has_wheeled
from merge import add_card_data

import numpy as np


# Only do the first 5
def compile_cards(
    df: pd.DataFrame,
    card_data: pd.DataFrame,
    columns_to_add: List[str],
    row: int,
    *,
    columns_for_average: Optional[List[str]] = None
) -> pd.DataFrame:
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

    # Extract scalar values
    draft_id = df["draft_id"].iloc[row]
    pack_number = df["pack_number"].iloc[row]
    pick_number = df["pick_number"].iloc[row]

    newdf["draft_id"] = draft_id
    newdf["pack_number"] = pack_number
    newdf["pick_number"] = pick_number
    newdf = newdf.set_index("name")

    newdf["has_wheeled"] = [
        has_wheeled(df, pack_number, pick_number, card_name)
        for card_name in newdf.index
    ]

    if columns_for_average is not None:
        for newrow in newdf.index:
            packs_without = df["cards_in_pack"][row].copy()
            packs_without.remove(newrow)
            packs_without = pd.DataFrame({"name": packs_without})
            packs_without = add_card_data(packs_without, card_data, columns_for_average)
            for col in columns_for_average:
                avg_col_name = col + "_avg"
                if avg_col_name not in newdf.columns:
                    newdf[avg_col_name] = None
                packs_without[col] = pd.to_numeric(packs_without[col], errors="coerce")
                newdf.at[newrow, avg_col_name] = packs_without[col].mean()

    return newdf
