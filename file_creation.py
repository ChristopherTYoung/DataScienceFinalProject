from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from io import StringIO
import pandas as pd
import requests
import time
import gzip
import os
import csv
from constants import (
    draft_data_file_name,
    draft_data_file_path,
    card_data_file_name,
    card_data_file_path,
    draft_url,
    card_data_url,
    draft_zip_file_name,
    mtg_set,
    format,
)


def create_draft_data_if_not_exists():
    if not os.path.exists(draft_data_file_path):
        print("Fetching data")
        response = requests.get(draft_url)
        with open(draft_zip_file_name, mode="wb") as file:
            file.write(response.content)

        with gzip.open(draft_zip_file_name, "rb") as f:
            file_content = f.read()
            with open(draft_data_file_name, "wb") as f_out:
                f_out.write(file_content)
    else:
        print("draft.csv already exists")


def create_card_data_if_not_exists():
    if not os.path.exists(card_data_file_path):
        print("Fetching card data...")
        fields = ["name", "mana_cost", "colors", "color_identity", "rarity"]

        with open(card_data_file_name, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            # Fetching all the pages of card data
            # The Scryfall API returns paginated results, so we need to loop through the pages
            next_url = card_data_url
            while next_url:
                response = requests.get(next_url)
                data = response.json()
                cards = data["data"]

                for card in cards:
                    writer.writerow({field: card.get(field, "") for field in fields})

                next_url = data.get("next_page") if data.get("has_more") else None

        add_card_statistics_to_card_data()
    else:
        print(f"{card_data_file_path} already exists")


def add_card_statistics_to_card_data():
    # Set up headless Chrome
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    url = f"https://www.17lands.com/card_data?expansion={mtg_set}&format={format}&start=2024-11-12&view=table"
    driver.get(url)

    card_df = pd.read_csv("./card_data.csv")

    time_to_sleep = 20
    print(
        f"Getting card statistics. Waiting for the page to load, this will take at least {time_to_sleep} seconds"
    )
    time.sleep(time_to_sleep)

    tables = pd.read_html(StringIO(driver.page_source))
    driver.quit()

    card_wr_df = tables[0]

    # Ensure the column names are standardized
    card_wr_df.columns = [col.strip() for col in card_wr_df.columns]

    # Extract only the necessary columns
    card_wr_df = card_wr_df[
        [col for col in card_wr_df.columns if col not in ["color", "rarity", "IWD"]]
    ]
    card_wr_df.rename(columns={"Name": "name"}, inplace=True)
    num_wr_cols = len(card_wr_df)

    print(
        "number of cards from the table (rows):",
        len(card_wr_df),
        "therefore there will be",
        num_wr_cols - len(card_df),
        "insignificant cards",
    )  # 281 for FDN

    # Remove percentage signs and convert to float
    percent_cols = [col for col in card_wr_df.columns if "%" in col]
    card_wr_df[percent_cols] = card_wr_df[percent_cols].apply(
        lambda x: x.str.rstrip("%").astype(float)
    )

    card_wr_df["name"] = card_wr_df["name"].str.lower()
    card_df["name"] = card_df["name"].str.lower()

    merged_df = pd.merge(card_df, card_wr_df, on="name", how="left")

    merged_df.to_csv("card_data.csv", index=False)
