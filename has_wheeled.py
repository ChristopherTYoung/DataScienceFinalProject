import pandas as pd


def has_wheeled(
    df_single_draft: pd.DataFrame,
    pack_number: int,
    pick_number: int,
    card_name: str,
) -> int:
    early_wheel_pairs = {0: 8, 1: 9, 2: 10, 3: 11, 4: 12, 5: 13}

    wheel_pick = early_wheel_pairs.get(pick_number)
    if wheel_pick is None:
        raise ValueError("Invalid pick number for early wheel.")

    match = df_single_draft[
        (df_single_draft["pack_number"] == pack_number)
        & (df_single_draft["pick_number"] == wheel_pick)
        & (df_single_draft["cards_in_pack"].apply(lambda cards: card_name in cards))
    ]

    return int(not match.empty)
