"""Entry point for the study bot."""
import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import db

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# Optional: set a test server ID so slash commands sync instantly while developing.
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

COGS = ["cogs.general", "cogs.tasks"]


class StudyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await db.init_db()
        for cog in COGS:
            await self.load_extension(cog)

        if DEV_GUILD_ID:
            guild = discord.Object(id=int(DEV_GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
        else:
            synced = await self.tree.sync()  # global sync can take up to an hour
        logging.info("Synced %d slash commands", len(synced))

    async def on_ready(self):
        logging.info("Logged in as %s (id %s)", self.user, self.user.id)


async def main():
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is missing. Copy .env.example to .env and fill it in.")
    async with StudyBot() as bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
