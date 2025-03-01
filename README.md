# DataForge

Datforge is a powerful data processing and transformation package designed for seamless data integration, manipulation, and analysis. It provides robust tools for handling large datasets efficiently. It to be used with the ebay app project to manage the different databases 

## Features

-High-performance data transformation

-Easy integration with databases and APIs

-Customizable processing pipelines

- Scalable and modular design

## Installation

'''
# Clone the repository
git clone https://github.com/yourusername/dataforge.git
cd dataforge

# Install package
pip install -e
'''

## Configuration

Before launching the package, ensure you have a .env file in the root directory with the following required variables:

'''
PROJECT_PATH="
#enpoints
API_MTGSTOCK_ENDPOINT = "https://api.mtgstocks.com/"
API_SCRYFALL_ENDPOINT = "https://api.scryfall.com/"

#Postgres related
POSTGRES_HOST  = 
POSTGRES_PASSWORD = 
POSTGRES_USER = 
DBNAME=

#MongoDB related
ULI = 
HIGHEST_VALID_ID='124910'
'''

## Options
The Datforge CLI provides several options for interacting with the databases for the eBay app:

'''
-l, --last [t|m]       The last MTGstock ID present in the table (t) or the valid ID for MTGstock (m)
-c, --count            Display the number of card entries in the card_id table
-u, --update [c|s]     Update the table with new entries if the last valid online is different from the last in the table
-v, --verbose          Prints more messages, useful for debugging
-q, --quiet            Suppresses the display of messages
x                     The size of each batch for API calls to MTGstock (default: 100)
'''