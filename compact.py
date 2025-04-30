def compact(df):
    pack_card_cols = [col for col in df.columns if col.startswith("pack_card_")]
    df["cards_in_pack"] = df[pack_card_cols].apply(
        lambda row: sum(
            [
                [col.replace("pack_card_", "")] * int(row[col])
                for col in pack_card_cols
                if row[col] > 0
            ],
            [],
        ),
        axis=1,
    )
    df = df.drop(columns=df.filter(like="pack_card_").columns)
    return df


# import pandas as pd
# from compile import compile_cards

# df = pd.DataFrame({
#     'user_id': [1, 2, 3],
#     'pack_card_a': [2, 1, 1],
#     'pack_card_b': [1, 1, 1],
#     'pack_card_c': [1, 1, 0],
#     'draft_id': [101, 101, 101],
#     'pack_number': [1, 1, 1],
#     'pick_number': [1, 2, 3]
# })
# card_data = pd.DataFrame({
#     'name': ['a', 'b', 'c'],
#     'mana_cost': ['1G', '2U', '3R'],
#     'color_identity': [['G'], ['U'], ['R']],
#     'rarity': ['common', 'uncommon', 'rare'],
#     '# Seen': [100, 80, 60],
#     'ALSA': [1.5, 2.1, 3.0],
#     '# Picked': [90, 60, 40],
#     'ATA': [1.4, 2.0, 2.9],
#     '# GP': [70, 50, 30],
#     '% GP': [70.0, 62.5, 50.0],
#     'GP WR': [55.2, 58.0, 53.3],
#     '# OH': [60, 45, 25],
#     'OH WR': [56.7, 60.1, 49.5],
#     '# GD': [40, 30, 15],
#     'GD WR': [54.0, 59.2, 50.0],
#     '# GIH': [85, 70, 50],
#     'GIH WR': [57.0, 61.0, 52.0],
#     '# GNS': [10, 12, 8],
#     'GNS WR': [48.0, 50.0, 45.0]
# })
# card_data.set_index('name')
# columns_to_add = [
#     'name',
#     'mana_cost',
#     'color_identity',
#     'rarity',
#     'GIH WR'
# ]
# compact(df)
# newdf = compile_cards(df, card_data, columns_to_add, 0, columns_for_average=['GIH WR'])
# print(newdf.head())
# print(df[["user_id", "cards_in_pack"]])
