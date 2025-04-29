import pandas as pd
# add columns color, rarity, mana cost, etc.
def add_card_data(df, card_data):
    combined_df = df.merge(card_data[['pick', 'mana_cost', 'color_identity', 'rarity']], 
                            on='pick', 
                            how='left')
    return combined_df