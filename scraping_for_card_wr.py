import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the 17Lands card data page
url = 'https://www.17lands.com/card_data?expansion=FDN&format=PremierDraft&start=2024-11-12&view=table'

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses


# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

print(soup)
# Find the table
table = soup.find('table')

print("Table found:", table is not None)

# Extract headers
headers = [th.text.strip() for th in table.find('thead').find_all('th')]

# Extract rows
rows = []
for tr in table.find('tbody').find_all('tr'):
    cells = [td.text.strip() for td in tr.find_all('td')]
    rows.append(cells)

# Create a DataFrame
df = pd.DataFrame(rows, columns=headers)

# Display the first few rows
print(df.head())
