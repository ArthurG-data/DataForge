import aiohttp, asyncio, json, os
from DataForge.functions.utils import get_header
from dotenv import load_dotenv

load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_PATH")


url = "https://api.scryfall.com/sets"

async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=get_header())  as response:
            if response.status == 200:
                response = await response.json()
                print(response)
                return response["data"]
            else:
                raise Exception(f"Error wihle downloading set database, {response.status}")
               

async def import_file(url, destination):
    try:
        json_file = await download_file(url)  

        
        with open(destination, 'w', encoding='utf-8') as f:
            json.dump(json_file, f, indent=4)

        print(f"File {destination} successfully replaced with new data")

    except Exception as e:
        print(f"Error downloading from {url} to {destination}: {e}")


destination = os.path.join(PROJECT_ROOT,"assets", "sets.json" )
print(destination)

asyncio.run(import_file(url, destination))