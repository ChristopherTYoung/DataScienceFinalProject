from typing import List, Optional
import pandas as pd
from has_wheeled import has_wheeled
from merge import add_card_data


# Only do the first 5
def compile_cards(
    df: pd.DataFrame,  # accept by entire drafts
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
    new_df = pd.DataFrame(
        {"name": [name.lower() for name in df["cards_in_pack"].loc[row]]}
    )
    new_df = add_card_data(new_df, card_data, columns_to_add)

    draft_id = df["draft_id"].loc[row]
    pack_number = df["pack_number"].loc[row]
    pick_number = df["pick_number"].loc[row]

    new_df["draft_id"] = draft_id
    new_df["pack_number"] = pack_number
    new_df["pick_number"] = pick_number
    new_df = new_df.set_index("name")

    new_df["has_wheeled"] = [
        has_wheeled(df, pack_number, pick_number, card_name)
        for card_name in new_df.index
    ]

    if columns_for_average is not None:
        for new_row in new_df.index:
            packs_without = df["cards_in_pack"][row].copy()
            packs_without.remove(new_row)
            packs_without = pd.DataFrame({"name": packs_without})
            packs_without = add_card_data(packs_without, card_data, columns_for_average)
            for col in columns_for_average:
                avg_col_name = col + "_avg"
                if avg_col_name not in new_df.columns:
                    new_df[avg_col_name] = None
                packs_without[col] = pd.to_numeric(packs_without[col], errors="coerce")
                new_df.at[new_row, avg_col_name] = packs_without[col].mean()

    return new_df


def compile_draft(
    df: pd.DataFrame, card_data: pd.DataFrame, *, picks_per_pack: int = 5
) -> pd.DataFrame:
    columns_to_add = ["name", "mana_cost", "color_identity", "rarity", "GIH WR"]
    result_frames = []
    unique_packs = [0, 1, 2]

    for pack in unique_packs:
        pack_rows = df[df["pack_number"] == pack]
        selected = pack_rows.nsmallest(picks_per_pack, "pick_number")
        for row_idx in selected.index:
            cards_df = compile_cards(
                df,
                card_data,
                columns_to_add,
                row_idx,
                columns_for_average=["GIH WR"],
            )
            result_frames.append(cards_df)

    if result_frames:
        out_df = pd.concat(result_frames).reset_index()
    else:
        out_df = pd.DataFrame()

    return out_df


def compile_all_drafts(
    big_df: pd.DataFrame,
    card_data: pd.DataFrame,
) -> pd.DataFrame:

    expanded_list = []
    for draft_id, draft_df in big_df.groupby("draft_id", sort=False):
        expanded = compile_draft(
            df=draft_df,
            card_data=card_data,
        )
        expanded_list.append(expanded)

    if expanded_list:
        all_expanded = pd.concat(expanded_list, ignore_index=True)
    else:
        all_expanded = pd.DataFrame()

    return all_expanded
