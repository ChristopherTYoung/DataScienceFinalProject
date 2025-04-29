import pandas as pd 


def compile_cards(df, row):
    newdf = pd.DataFrame({"name": df["cards_in_pack"][row]})
    
    return newdf