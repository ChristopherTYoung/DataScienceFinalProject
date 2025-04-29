from typing import List
import pandas as pd

def clean_nulls_care(mtgdraft: pd.DataFrame, columns_list: List[str]) -> pd.DataFrame:
    hasmissing = mtgdraft[columns_list].isna().any(axis=1)
    return mtgdraft[~hasmissing]

def remove_incomplete(mtgdraft: pd.DataFrame) -> pd.DataFrame:
    grouped = mtgdraft.groupby("draft_id").size()
    incompletedrafts = grouped[grouped!=36]
    return mtgdraft[~mtgdraft["draft_id"].isin(incompletedrafts.index)]
