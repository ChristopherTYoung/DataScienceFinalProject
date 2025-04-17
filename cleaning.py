def clean_nulls_care(mtgdraft, columns_list):
    hasmissing = mtgdraft[columns_list].isna().any(axis=1)
    return mtgdraft[~hasmissing]

def remove_incomplete(mtgdraft):
    grouped = mtgdraft.groupby("draft_id").size()
    incompletedrafts = grouped[grouped!=36]
    return mtgdraft[~mtgdraft["draft_id"].isin(incompletedrafts.index)]
