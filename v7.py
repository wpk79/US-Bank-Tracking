import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# Function to fetch and process a specific table
def fetch_table(soup, table_index):
    # Find all tables in the webpage
    tables = soup.find_all('table')

    # Get the specified table
    table_html = str(tables[table_index])

    # Use StringIO to wrap the HTML string
    table_io = StringIO(table_html)

    # Use pandas to read the HTML table
    df = pd.read_html(table_io)[0]

    # Set the first column as the index (assuming it contains the item names)
    df.set_index(df.columns[0], inplace=True)

    # Rename the index
    df.index.name = 'Item'

    return df

# Main function to fetch and process the data
def fetch_and_save_data():
    # URL for the current data
    url = 'https://www.federalreserve.gov/releases/h8/current/default.htm'

    # Fetch the webpage
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Fetch Table 2 and select items 1, 3, 9, 10, 20, and 34
    df_table_2 = fetch_table(soup, 1)
    selected_items_table_2 = ['1', '3', '9', '10', '20', '34']
    df_selected_table_2 = df_table_2.loc[selected_items_table_2]

    # Fetch Table 8 and select item 34
    df_table_8 = fetch_table(soup, 7)
    selected_items_table_8 = ['34']
    df_selected_table_8 = df_table_8.loc[selected_items_table_8]

    # Combine the selected items from both tables
    df_combined = pd.concat([df_selected_table_2, df_selected_table_8])

    # Print the combined DataFrame to the console
    print("\nCombined DataFrame:")
    print(df_combined.to_string())

    # Save the combined DataFrame to an Excel file
    df_combined.to_excel("US Banking Raw.xlsx", index=True)

    print("\nData has been successfully saved to 'US Banking Raw.xlsx'.")

# Fetch and save the data
fetch_and_save_data()
