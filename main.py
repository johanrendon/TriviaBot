"""Main entry point for the Discord bot.

This script initializes the bot, sets up logging, loads environment variables,
configures Discord intents, loads all command extensions (cogs), and runs
the bot.
"""

import asyncio
import logging
import os
from typing import Final

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import PREFIX

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv()
TOKEN: Final[str] = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


async def load_cogs() -> None:
    """Dynamically finds and loads all cogs from the '/cogs' directory.

    This function iterates through all files in the './cogs' directory.
    If a file ends with '.py', it attempts to load it as a bot extension.
    It logs the outcome (success or failure) for each cog.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"✅ Cog loaded: {filename}")
            except Exception as e:
                logging.error(f"❌ Error loading {filename}: {e}")


@bot.event
async def on_ready() -> None:
    """Event handler that runs when the bot successfully connects to Discord.

    Logs a confirmation message to the console and sets the bot's presence
    to "Playing Trivia!".
    """
    logging.info(f"Bot connected as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Trivia!"))


async def main() -> None:
    """The main asynchronous function to run the bot.

    This function serves as the primary entry point. It loads all cogs
    and then starts the bot, connecting it to Discord using the token from
    the environment variables.
    """
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
