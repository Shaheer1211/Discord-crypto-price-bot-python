#You will have to install pip packages for discord and requests

import discord
import requests
import asyncio
import logging

coin_tokens_price = {
    # Your discord tokens here as a dictionary, can be multiple check discords doc for rate limit
}

# API powered by CoinGecko
async def update_crypto_price(coin):
    URL = f'https://api.coingecko.com/api/v3/coins/{coin}'
    r = requests.get(url=URL)
    data = r.json()
    return [data['market_data']['current_price']['usd'], data['symbol']]

async def get_crypto_price(coin):
    return await update_crypto_price(coin)

async def run_bot(coin, token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"You have logged in as {client.user}")

        while True:
            try:
                await asyncio.sleep(30)
                price_cap = await get_crypto_price(coin)
                price = price_cap[0]
                symbol = price_cap[1]
                nickname = f"{symbol.upper()} ~ ${price}"
                print(nickname)
                for guild in client.guilds:
                    await guild.me.edit(nick=nickname)
            except discord.DiscordException as e:
                logging.error(f"An error occurred: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")

    await client.start(token)

async def main():
    tasks = []
    for coin, token in coin_tokens_price.items():
        tasks.append(asyncio.create_task(run_bot(coin, token)))
    await asyncio.gather(*tasks)

logging.basicConfig(level=logging.ERROR)
asyncio.run(main())
