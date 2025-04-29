def compact(df):
    pack_card_cols = [col for col in df.columns if col.startswith('pack_card_')]
    df['cards_in_pack'] = df[pack_card_cols].apply(
    lambda row: [col.replace("pack_card_", "") for col in pack_card_cols if row[col]], axis=1
    )
    return df


import pandas as pd
from compile import compile_cards

df = pd.DataFrame({
    'user_id': [1, 2, 3],
    'pack_card_a': [True, False, True],
    'pack_card_b': [False, True, False],
    'pack_card_c': [True, True, False],
    'other_col': ['x', 'y', 'z']
})

compact(df)
newdf = compile_cards(df, 0)
print(newdf.head())
print(df[['user_id', 'cards_in_pack']])