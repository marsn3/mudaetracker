import discord
from discord.ext import commands
from config import TOKEN, PREFIX

bot = commands.Bot(command_prefix=PREFIX, description="Track the Top-1000 of Mudae")
if __name__ == "__main__":
    bot.load_extension("mudaetracker")


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


bot.run(TOKEN, bot=True, reconnect=True)
