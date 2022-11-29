import discord
from discord.ext import commands
from config import TOKEN, PREFIX
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=PREFIX,
    description="Track the Top-1000 of Mudae",
    intents=intents,
)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


async def load():
    await bot.load_extension("mudaetracker")


# client connect
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)


asyncio.run(main())
