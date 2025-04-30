from typing import List, Optional
import pandas as pd
from has_wheeled import has_wheeled
from merge import add_card_data


def compile_cards(
    df: pd.DataFrame,
    card_data: pd.DataFrame,
    columns_to_add: List[str],
    row: int,
    *,
    columns_for_average: Optional[List[str]] = None
) -> pd.DataFrame:
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

    # ✅ Use scalar values in has_wheeled()
    newdf["has_wheeled"] = [
        has_wheeled(df, pack_number, pick_number, card_name)
        for card_name in newdf.index
    ]

    if columns_for_average is not None:
        for newrow in newdf.index:
            packs_without = df["cards_in_pack"][row].copy()
            packs_without.remove(newrow)
            packs_without = pd.DataFrame({"name": packs_without})
            packs_without = add_card_data(
                packs_without, card_data, ["name"] + columns_for_average
            )

            for col in columns_for_average:
                avg_col_name = col + "_avg"
                if avg_col_name not in newdf.columns:
                    newdf[avg_col_name] = None

                newdf.at[newrow, avg_col_name] = packs_without[col].mean()

    return newdf
