import pandas as pd
# add columns color, rarity, mana cost, etc.
def add_card_data(df, card_data, columns_to_add):
    combined_df = df.merge(card_data[columns_to_add], 
                            on='name', 
                            how='left')
    return combined_df