import pandas as pd 


def compile_cards(df: pd.DataFrame, row) -> pd.DataFrame:
    new_df = pd.DataFrame({"name": df["cards_in_pack"][row]})
    
    return new_df