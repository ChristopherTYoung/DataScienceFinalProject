draft_data_file_name = "draft.csv"
draft_data_file_path = f"./{draft_data_file_name}"

card_data_file_name = "card_data.csv"
card_data_file_path = f"./{card_data_file_name}"

mtg_set = "FDN"
mtg_set_for_card_data = mtg_set.lower()

format = "PremierDraft"
draft_zip_file_name = f"draft_data_public.{mtg_set}.{format}.csv.gz"
draft_url = f"https://17lands-public.s3.amazonaws.com/analysis_data/draft_data/{draft_zip_file_name}"
card_data_url = f"https://api.scryfall.com/cards/search?q=set:{mtg_set_for_card_data}"
