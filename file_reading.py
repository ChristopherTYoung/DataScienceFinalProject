from typing import List
import pandas as pd
from constants import draft_data_file_name


def read_draft_data(columns_to_use: List[str]) -> pd.DataFrame:
    chunk_size = 100
    total_chunks = 1
    total_number_of_rows = chunk_size * total_chunks
    number_of_rows_processed = 0

    chunks = []

    for chunk in pd.read_csv(
        draft_data_file_name, usecols=columns_to_use, chunksize=chunk_size
    ):
        number_of_rows_processed += chunk_size
        print(
            f"processed (another) {number_of_rows_processed} rows out of {total_number_of_rows}"
        )
        filtered_chunk = chunk[
            (chunk["pick_number"] != 6) & (chunk["pick_number"] != 7)
        ]
        chunks.append(filtered_chunk)
        if number_of_rows_processed >= total_number_of_rows:
            break

    return pd.concat(chunks, ignore_index=True)


def get_necessary_col_names_from_csv(file_name: str) -> List[str]:
    df = pd.read_csv(file_name, nrows=0)
    return [
        *[col for col in df.columns if col.startswith("pack_card_")],
        "draft_id",
        "pack_number",
        "pick_number",
        "pick",
    ]
