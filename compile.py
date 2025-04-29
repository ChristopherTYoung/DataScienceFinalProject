import pandas as pd 
from merge import add_card_data

def compile_cards(df, card_data, columns_to_add, row):
    newdf = pd.DataFrame({"name": df["cards_in_pack"][row]})
    newdf = add_card_data(newdf, card_data, columns_to_add)
    newdf["draft_id"], newdf["pack_number"], newdf["pick_number"] = df["draft_id"].iloc[row], df["pack_number"].iloc[row], df["pick_number"].iloc[row]
    return newdf