# Fall 2025 Intro Into Data Science Final

### Christopher Young

### Nathan Howell

### Benson Bird

## List of ideas for Regression variables

- Mana cost
- Color Identity
- Rarity
- Number of cards of similar color in the pack
- Game in hand win rate
- What cards wheeled in previous drat packs (colors)
- Median of other cards GIHWR

# Notes about project

There are some cards (FDN has 236) that are 'Underrepresented'
This means that we do not have enough data to create the stats wanted for specific cards.
To put this in perspective, FDN has 500+ cards in the set, but only about 280 cards have enough data to create the stats we want

# Requirements

### Acquire data using web scraping or APIs

We have three examples of this.

We scrape [this website choosing the FDN set, Premier Draft Format, and the Draft data](https://www.17lands.com/public_datasets).

Here is the line we do it on:  
We scrape the same website, but a different page and data here: [17lands FDN Premier Data](https://www.17lands.com/card_data?expansion=FDN&format=PremierDraft&view=table&start=2024-11-12).

[See lines 24 - 36 of this file](https://github.com/ChristopherTYoung/DataScienceFinalProject/blob/main/file_creation.py#L24-L36)

```
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
```

We are allowed to do this through their license: [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0/).  
You can find that on the first link listed, the one where we find our public datasets.

[See lines 40 - 59 of this file](https://github.com/ChristopherTYoung/DataScienceFinalProject/blob/main/file_creation.py#L40-L59)

```
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
```

We are also scraping [Scryfall API](https://scryfall.com/) specifically the [FDN set and utilize it's pagination](https://api.scryfall.com/cards/search?q=set:FDN).

We are allowed to do this through the Wizards of the Coast policy: [Wizards Fan Content Policy](https://company.wizards.com/en/legal/fancontentpolicy).  
You can find that here on Scryfall: [Scryfall API Documentation](https://scryfall.com/docs/api).

[See lines 67 - 96 of this file](https://github.com/ChristopherTYoung/DataScienceFinalProject/blob/main/file_creation.py#L67-L96)

```
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
```
