from typing import List
import pandas as pd


def get_necessary_col_names_from_csv(file_name: str) -> List[str]:
    df = pd.read_csv(file_name, nrows=0)
    return [
        *[col for col in df.columns if col.startswith("pack_card_")],
        "draft_id",
        "pack_number",
        "pick_number",
        "pick"
    ]
