from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

url = "https://www.17lands.com/card_data?expansion=FDN&format=PremierDraft&start=2024-11-12&view=table"
driver.get(url)

card_df = pd.read_csv("./card_data.csv")

# Wait for the page to load completely
time.sleep(20)

tables = pd.read_html(driver.page_source)
driver.quit()

card_wr_df = tables[0]

# Ensure the column names are standardized
card_wr_df.columns = [col.strip() for col in card_wr_df.columns]

# Extract only the necessary columns
card_wr_df = card_wr_df[
    [col for col in card_wr_df.columns if col not in ["color", "rarity"]]
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

# Standardize the card names to lowercase for consistent merging
card_wr_df["name"] = card_wr_df["name"].str.lower()
card_df["name"] = card_df["name"].str.lower()

merged_df = pd.merge(card_df, card_wr_df, on="name", how="left")

merged_df.to_csv("card_data.csv", index=False)
