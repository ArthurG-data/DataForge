import aiohttp, asyncio
from database_manager.functions.utils import get_header


async def download_sets():
    url = "https://api.scryfall.com/sets"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=get_header())  as response:
            if response.status == 200:
                return await response.json
            else:
                print(f"Error wihle downloading set database, {response.status}")
                return None
            

asyncio.run(download_sets())