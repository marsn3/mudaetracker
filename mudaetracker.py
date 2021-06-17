import discord
from discord.ext import commands
from discord.ext import tasks
import csv
from asyncio import sleep
from browsers import Browser
from random import randrange
from config import CHANNEL_ID, PAGES, HOURS, SERVER_ID, MUDAE, IM_LIST, MUDAE_PREFIX
import os
import arrow
import re

browser = Browser()


class MudaeTracker(commands.Cog):
    """
    Various tasks that run in the background
    """

    def __init__(self, bot):
        self.bot = bot
        self.top_path = "top1000.csv"
        if not os.path.exists(str(self.top_path)):
            with open(str(self.top_path), "w", newline="", encoding="utf-8") as csvfile:
                c = csv.writer(csvfile)
                c.writerow(["rank", "name", "series", "date"])
        if os.path.exists(IM_LIST):

            self.im_path = "im_chars.csv"
            if not os.path.exists(str(self.im_path)):
                with open(
                    str(self.im_path), "w", newline="", encoding="utf-8"
                ) as csvfile:
                    c = csv.writer(csvfile)
                    c.writerow(
                        ["claimrank", "likerank", "kakera", "name", "series", "time"]
                    )
            self.im.start()
        self.top.start()

    def cog_unload(self):
        self.top.cancel()
        browser.close()

    def clean_top_embed(self, message: discord.Message):
        embed = message.embeds[0]
        results = []
        if embed.description:
            content = discord.utils.remove_markdown(embed.description)
            content = content.replace("  ", "")
            content = content.replace("#", "")
            content = content.replace("\u200b\n", "")
            content = content.strip()
            content = content.split("\n")
            for line in content:
                time = arrow.utcnow().format("YYYY.MM.DD")
                line += f" - {time}"
                column = line.split(" - ")
                column = [e.strip() for e in column]
                if column not in results:
                    results.append(column)
            return results

    def clean_im_embed(self, message: discord.Message):
        embed = message.embeds[0]
        if embed.description:
            name = embed.author.name
            kakera = re.search(r"\*\*(\d*)", embed.description, re.DOTALL).group(1)
            claimrank = re.search(
                r"Claim Rank:\ \#(\d*).*?", embed.description, re.DOTALL
            ).group(1)
            likerank = re.search(
                r"Like Rank:\ \#(\d*)", embed.description, re.DOTALL
            ).group(1)
            series = (
                re.search(r"(.+?(?=<:.*male))", embed.description, re.DOTALL)
                .group(1)
                .strip()
            )
            time = arrow.utcnow().format("YYYY.MM.DD")
            results = [claimrank, likerank, kakera, name, series, time]
            return results

    def write_csv(self, file, message: discord.message):
        if file == self.top_path:
            with open(str(file), "a", newline="", encoding="utf-8") as csvfile:
                c = csv.writer(csvfile)
                results = self.clean_top_embed(message)
                for column in results:
                    c.writerow(column)
        elif file == self.im_path:
            with open(str(file), "a", newline="", encoding="utf-8") as csvfile:
                c = csv.writer(csvfile)
                results = self.clean_im_embed(message)
                c.writerow(results)

    @commands.command()
    async def csv(self, ctx: commands.Context):
        """
        Upload CSV
        """
        await ctx.send(file=discord.File(fp=self.top_path))
        if os.path.exists(self.im_path):
            await ctx.send(file=discord.File(fp=self.im_path))

    @tasks.loop(hours=HOURS)
    async def top(self):
        try:
            browser.browser_login(browser)
            for i in range(1, PAGES + 1):
                Browser.send_text(browser, f"{MUDAE_PREFIX}top {i}")
                await sleep(randrange(2, 10))
        except TimeoutError:
            browser.close()

    @tasks.loop(hours=HOURS)
    async def im(self):
        try:
            browser.browser_login(browser)
            for character in open("im_list.txt"):
                Browser.send_text(browser, f"{MUDAE_PREFIX}im {character}")
                await sleep(randrange(2, 10))
        except TimeoutError:
            browser.close()

    @top.before_loop
    async def before_top(self):
        await self.bot.wait_until_ready()

    @im.before_loop
    async def before_top(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == SERVER_ID:
            if message.channel.id == CHANNEL_ID:
                if message.author == await self.bot.fetch_user(MUDAE):
                    if message.embeds:
                        if message.embeds[0].author.name == "🏆 TOP 1000":
                            self.write_csv(self.top_path, message)
                        elif "Claim Rank" in message.embeds[0].description:
                            self.write_csv(self.im_path, message)


def setup(bot):
    bot.add_cog(MudaeTracker(bot))
