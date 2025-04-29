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

There are some cards (FND has 236) that are 'Underrepresented'
This means that we do not have enough data to create the stats wanted for specific cards.
To put this in perspective, FND has 500+ cards in the set, but only about 280 cards have enough data to create the stats we want

# Requirements

### Acquire data using web scraping or APIs

We have three examples of this.
We scrape (https://www.17lands.com/public_datasets)[https://www.17lands.com/public_datasets]
We scrape the same website, but different page and data here (https://www.17lands.com/card_data?expansion=FDN&format=PremierDraft&view=table&start=2024-11-12)[https://www.17lands.com/card_data?expansion=FDN&format=PremierDraft&view=table&start=2024-11-12]

We are allowed to do this through their license: (https://creativecommons.org/licenses/by/4.0/)[https://creativecommons.org/licenses/by/4.0/]
You can find that on the first link listed, the one where we find our public datasets

We also scraping Scryfall's Api: (https://scryfall.com/)[https://scryfall.com/]

We are allowed to do this through the Wizards of the coast policy: (https://company.wizards.com/en/legal/fancontentpolicy)[https://company.wizards.com/en/legal/fancontentpolicy]
You can find that here on Scryfall: (https://scryfall.com/docs/api)[https://scryfall.com/docs/api]
