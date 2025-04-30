from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from io import StringIO
import pandas as pd
import requests
import time
import gzip
import os
import csv
import re
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
        print(f"{draft_data_file_name} already exists")


def create_card_data_if_not_exists():
    if not os.path.exists(card_data_file_path):
        print("Fetching card data...")
        fields = ["name", "mana_cost", "colors", "color_identity", "rarity", "price"]

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
                    writer.writerow(
                        {
                            "name": card.get("name", ""),
                            "mana_cost": mana_cost_to_value(card.get("mana_cost", "")),
                            "colors": ",".join(card.get("colors", [])),
                            "color_identity": ",".join(card.get("color_identity", [])),
                            "rarity": card.get("rarity", ""),
                            "price": float(card.get("prices", {}).get("usd") or 0),
                        }
                    )

                next_url = data.get("next_page") if data.get("has_more") else None

        add_card_statistics_to_card_data()
    else:
        print(f"{card_data_file_path} already exists")


def add_card_statistics_to_card_data():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    url = f"https://www.17lands.com/card_data?expansion={mtg_set}&format={format}&view=table"
    driver.get(url)

    card_df = pd.read_csv(card_data_file_name)

    is_table_ready = False
    timeout = 30  # Timeout after 30 seconds if table is not found
    start_time = time.time()

    while not is_table_ready:
        try:
            tables = pd.read_html(StringIO(driver.page_source))
            card_wr_df = tables[0]

            if not card_wr_df.empty:
                is_table_ready = True
            else:
                raise ValueError("Table is empty, retrying.")
        except (ValueError, IndexError) as e:
            if time.time() - start_time > timeout:
                print("Timeout reached, unable to find valid table.")
                break
            time.sleep(1)
            print("Waiting for table to load...")

    driver.quit()

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
        len(card_df) - num_wr_cols,
        "insignificant cards",
    )

    card_wr_df["name"] = card_wr_df["name"].str.lower()
    card_df["name"] = card_df["name"].str.lower()

    card_df["mana_cost"] = card_df["mana_cost"].apply(mana_cost_to_value)

    merged_df = pd.merge(card_df, card_wr_df, on="name", how="left")

    merged_df.to_csv(card_data_file_name, index=False)


def mana_cost_to_value(mana_cost: str) -> int:
    if not isinstance(mana_cost, str):
        return 0

    if not mana_cost:
        return 0

    # Find all symbols like {1}, {R}, {U}, etc.
    symbols = re.findall(r"\{(.*?)\}", mana_cost)
    total = 0

    for symbol in symbols:
        if symbol.isdigit():
            total += int(symbol)
        else:
            total += 1

    return total
