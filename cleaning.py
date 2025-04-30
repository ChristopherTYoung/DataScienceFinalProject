from typing import List
import pandas as pd

def clean_nulls_care(mtgdraft: pd.DataFrame, columns_list: List[str]) -> pd.DataFrame:
    """
    Removes rows from the DataFrame where any specified columns contain null values.

    Args:
        mtgdraft (pd.DataFrame): The input DataFrame to clean.
        columns_list (List[str]): List of column names to check for null values.

    Returns:
        pd.DataFrame: A DataFrame with rows containing null values in the specified columns removed.
    """
    hasmissing = mtgdraft[columns_list].isna().any(axis=1)
    return mtgdraft[~hasmissing]

def remove_incomplete(mtgdraft: pd.DataFrame) -> pd.DataFrame:
    """
    Removes draft records where the number of picks is not equal to 36.

    This function assumes that each draft should have exactly 36 picks. Drafts with a different number 
    of picks are removed from the DataFrame.

    Args:
        mtgdraft (pd.DataFrame): The input DataFrame containing draft data.

    Returns:
        pd.DataFrame: A DataFrame with drafts containing less than or greater than 36 picks removed.
    """
    grouped = mtgdraft.groupby("draft_id").size()
    incompletedrafts = grouped[grouped!=36]
    return mtgdraft[~mtgdraft["draft_id"].isin(incompletedrafts.index)]
